# Kubernetes Manifests - Plain YAML

Raw Kubernetes manifests for deploying Pamawas services. Assumes you have deployed the observability stack (PostgreSQL, Prometheus, Loki, Tempo, Grafana) separately.

## Prerequisites (Deploy Separately)

| Component | Recommended Deployment |
|-----------|------------------------|
| **PostgreSQL** | Cloud SQL, RDS, `bitnami/postgresql` Helm, `cnpg` operator |
| **Prometheus** | `prometheus-community/kube-prometheus-stack` |
| **Loki** | `grafana/loki-stack` Helm, Grafana Agent |
| **Tempo** | `grafana/tempo` Helm, Grafana Agent |
| **Grafana** | Included in kube-prometheus-stack |

## Quick Start

```bash
cd k8s
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployments/
kubectl apply -f services.yaml
kubectl apply -f servicemonitor.yaml
kubectl apply -f ingress.yaml
```

## Configuration

### ConfigMap (configmap.yaml)
Non-sensitive configuration for all services. Update endpoints for your environment:
- `OTEL_EXPORTER_OTLP_ENDPOINT`: Tempo OTLP gRPC endpoint
- `PROMETHEUS_URL`, `LOKI_URL`: Observability stack endpoints
- Service-specific configs (correlator time window, scheduler times, etc.)

### Secret (secret.yaml)
Sensitive values. **Replace all placeholder values** before applying:
- `DATABASE_URL`: PostgreSQL connection string with credentials
- `LLM_API_KEY`: OpenAI/Anthropic/Ollama API key
- Delivery credentials (Discord, Telegram, Email)
- `REPORT_TEMPLATE`: Optional custom report template

## Services Deployed

| Service | Replicas | Port | Health Checks |
|---------|----------|------|---------------|
| pamawas-ingest | 2 | 8080 | /healthz, /ready |
| pamawas-correlator | 1 | 8080 | /healthz, /ready |
| pamawas-investigator | 1 | 8080 | /healthz, /ready |
| pamawas-reporter | 1 | 8080 | /healthz, /ready |
| pamawas-scheduler | 1 | 8080 | /healthz, /ready |
| pamawas-schema-migration | Job | 8080 | N/A |

## Observability

All services include:
- **Prometheus annotations** for auto-scraping (`/metrics`)
- **ServiceMonitors** for Prometheus Operator
- **Structured JSON logging** with trace_id/span_id
- **OpenTelemetry tracing** to Tempo (OTLP gRPC)
- **Health/Readiness endpoints** for Kubernetes probes

## Ingress

Ingress configured for nginx with TLS via cert-manager. Update `pamawas.example.com` to your domain.

```yaml
# ingress.yaml paths
/webhook*        -> pamawas-ingest
/healthz, /ready -> pamawas-ingest
/trigger*        -> pamawas-correlator
/status          -> pamawas-correlator
/investigate*    -> pamawas-investigator
/report*         -> pamawas-reporter
/trigger/daily   -> pamawas-scheduler
/trigger/high-severity -> pamawas-scheduler
```

## ServiceAccount

All pods use `pamawas` ServiceAccount. Ensure RBAC is configured if needed.

## Network Policies

Not included by default. Add NetworkPolicies to restrict traffic between services if required.

## Updating Deployments

```bash
# Update image tags in deployment files, then:
kubectl apply -f k8s/deployments/

# Or use kubectl set image:
kubectl set image deployment/pamawas-ingest ingest=ghcr.io/pamawas/pamawas-ingest:v1.2.3 -n pamawas
```

## Cleanup

```bash
kubectl delete -f k8s/
```