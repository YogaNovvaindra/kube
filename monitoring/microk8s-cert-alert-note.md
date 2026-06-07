# MicroK8s Certificate Expiry — Alert Setup

## Architecture

```
x509-certificate-exporter (DaemonSet, kube-1)
  → mounts /var/snap/microk8s/current/certs/ (hostPath)
  → reads *.crt files directly
  → exposes x509_cert_not_after{filepath=...} (unix timestamp)
  → Prometheus scrapes & evaluates alert rules
  → Grafana for visualization only
```

> **Key principle**: Alerting belongs in **Prometheus rules**, not Grafana.
> Prometheus rules fire even if Grafana is down.

---

## File 1 — `monitoring/x509-exporter.yml` [NEW]

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: x509-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: x509-exporter
  template:
    metadata:
      labels:
        app: x509-exporter
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9793"
    spec:
      nodeSelector:
        kubernetes.io/hostname: kube-1
      tolerations:
        - operator: Exists
      hostNetwork: true
      containers:
        - name: x509-exporter
          image: ghcr.io/enix/x509-certificate-exporter:3
          imagePullPolicy: IfNotPresent
          args:
            - --watch-file=/host-certs/ca.crt
            - --watch-file=/host-certs/server.crt
            - --watch-file=/host-certs/front-proxy-client.crt
            - --watch-file=/host-certs/front-proxy.crt
            - --watch-file=/host-certs/apiserver-kubelet-client.crt
            - --listen-address=:9793
          ports:
            - containerPort: 9793
              name: metrics
          resources:
            requests:
              cpu: 10m
              memory: 16Mi
            limits:
              memory: 32Mi
          volumeMounts:
            - name: microk8s-certs
              mountPath: /host-certs
              readOnly: true
      volumes:
        - name: microk8s-certs
          hostPath:
            path: /var/snap/microk8s/current/certs
            type: Directory
---
apiVersion: v1
kind: Service
metadata:
  name: x509-exporter
  namespace: monitoring
spec:
  selector:
    app: x509-exporter
  ports:
    - port: 9793
      targetPort: 9793
      name: metrics
```

---

## File 2 — `monitoring/prometheus/alert-rules-certs.yml` [NEW]

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-alert-rules-certs
  namespace: monitoring
data:
  cert-alerts.yml: |
    groups:
      - name: certificate_expiry
        rules:

          - alert: CertificateExpiryWarning
            expr: |
              (x509_cert_not_after - time()) / 86400 < 30
            for: 1h
            labels:
              severity: warning
            annotations:
              summary: "Certificate expiring soon on {{ $labels.node }}"
              description: >
                Certificate {{ $labels.filepath }} expires in
                {{ $value | printf "%.0f" }} days.
                Run: ssh root@10.1.1.11 "sudo microk8s refresh-certs --check"

          - alert: CertificateExpiryCritical
            expr: |
              (x509_cert_not_after - time()) / 86400 < 7
            for: 10m
            labels:
              severity: critical
            annotations:
              summary: "Certificate expiring in < 7 days on {{ $labels.node }}"
              description: >
                URGENT: {{ $labels.filepath }} expires in {{ $value | printf "%.0f" }} days.
                Run: ssh root@10.1.1.11 "sudo microk8s refresh-certs -e 168h && sudo microk8s stop && sudo microk8s start"

          - alert: CertificateExpired
            expr: |
              x509_cert_not_after - time() < 0
            for: 0m
            labels:
              severity: critical
            annotations:
              summary: "Certificate EXPIRED on {{ $labels.node }}"
              description: >
                Certificate {{ $labels.filepath }} has EXPIRED.
                Cluster auth is broken. Renew immediately.
```

---

## File 3 — Modify `monitoring/prometheus/prometheus-config.yml`

### Add `rule_files` at the top of `prometheus.yml` (before `scrape_configs`):

```yaml
rule_files:
  - /etc/prometheus/rules/**/*.yml
```

### Add scrape job under `scrape_configs`:

```yaml
      - job_name: x509_exporter
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names: [monitoring]
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: x509-exporter
          - source_labels: [__meta_kubernetes_pod_ip]
            target_label: __address__
            replacement: $1:9793
          - source_labels: [__meta_kubernetes_pod_node_name]
            target_label: node
```

---

## File 4 — Modify `monitoring/prometheus/prometheus-deploy.yml`

### Add to `volumes`:
```yaml
- name: alert-rules-certs
  configMap:
    name: prometheus-alert-rules-certs
```

### Add to prometheus container `volumeMounts`:
```yaml
- name: alert-rules-certs
  mountPath: /etc/prometheus/rules/certs
  readOnly: true
```

---

## File 5 — Auto-renewal script on kube-1 [NEW]

Deploy to `/usr/local/bin/microk8s-cert-renew.sh` on kube-1:

```bash
#!/bin/bash
# Renews MicroK8s certs expiring within 30 days. Run monthly via cron.
set -euo pipefail

LOG_PREFIX="[$(date -u +%Y-%m-%dT%H:%M:%SZ)]"
THRESHOLD_HOURS=$((30 * 24))

output=$(microk8s refresh-certs --check 2>&1)

if echo "$output" | grep -qP 'expire in [0-9]{1,2} days'; then
  echo "$LOG_PREFIX Certs expiring soon — renewing..."
  microk8s refresh-certs -e "${THRESHOLD_HOURS}h"
  microk8s stop && microk8s start
  echo "$LOG_PREFIX Renewal complete."
else
  echo "$LOG_PREFIX All certs healthy, no renewal needed."
fi
```

Crontab on kube-1 (runs on the 1st of every month):
```
0 2 1 * * /usr/local/bin/microk8s-cert-renew.sh >> /var/log/microk8s-cert-renew.log 2>&1
```

---

## Grafana Dashboard

```promql
# Days until expiry per cert
(x509_cert_not_after{job="x509_exporter"} - time()) / 86400
```

- Visualization: `Bar gauge`
- Unit: `days (d)`
- Thresholds: Green `> 30` / Yellow `> 7` / Red `≤ 7`
- Community dashboard import ID: **13922**

---

## Summary of Changes

| File | Action |
|---|---|
| `monitoring/x509-exporter.yml` | [NEW] DaemonSet + Service |
| `monitoring/prometheus/alert-rules-certs.yml` | [NEW] Prometheus alert rules ConfigMap |
| `monitoring/prometheus/prometheus-config.yml` | [MODIFY] add `rule_files` + scrape job |
| `monitoring/prometheus/prometheus-deploy.yml` | [MODIFY] mount alert-rules ConfigMap |
| `kube-1:/usr/local/bin/microk8s-cert-renew.sh` | [NEW] auto-renewal script |

## Renewal Runbook (when alert fires)

```bash
ssh root@10.1.1.11

# Check which certs are affected
sudo microk8s refresh-certs --check

# Renew all certs expiring within 30 days
sudo microk8s refresh-certs -e 720h

# Restart MicroK8s
sudo microk8s stop && sudo microk8s start

# Refresh local kubeconfig on Windows
ssh root@10.1.1.11 "microk8s config" | Set-Content "$env:USERPROFILE\.kube\config"
```
