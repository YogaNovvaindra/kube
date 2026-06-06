# 🚀 Application Services

This directory contains various personal and application services running in the cluster.

## 🌟 Featured Services

| Service | File | Description |
|---------|------|-------------|
| **Ghost** | [`ghost/ghost.yml`](ghost/ghost.yml) | Professional publishing platform and blog |
| **Portfolio** | [`portfolio/portfolio.yml`](portfolio/portfolio.yml) | Personal project showcase (Auto-scales via HPA) |
| **Linear Next** | [`linear-next/linear-next.yml`](linear-next/linear-next.yml) | Issue tracking and project management |
| **EcoGuardian** | [`ecoguardian/ecoguardian.yml`](ecoguardian/ecoguardian.yml) | Environmental monitoring service |
| **Tolonto** | [`tolonto/tolonto.yml`](tolonto/tolonto.yml) | PHP LAMP development stack |

## 🔗 Shared Resources & Utilities

- **[`db-backup/db-backup.yml`](db-backup/db-backup.yml)**: Generic, automated multi-database backup CronJob configuration (backs up MySQL, PostgreSQL).
- **[`discord/discord-cred.yml`](discord/discord-cred.yml)**: Shared Discord webhook credentials for service alerts.

## ☁️ Cloudflare Tunnel Routing

This cluster uses the **Cloudflare Operator** (`ClusterTunnel` and `TunnelBinding` CRDs) to securely expose services to the internet, rather than running a manual `cloudflared` deployment. 

Most services in this directory (e.g., Portfolio, Linear Next, Tolonto) have a `TunnelBinding` resource defined in their YAML file that automatically routes their `fqdn` to their internal Kubernetes Service.

### Example TunnelBinding:

```yaml
apiVersion: networking.cfargotunnel.com/v1alpha1
kind: TunnelBinding
metadata:
  name: example-binding
  namespace: services
subjects:
  - name: example-service
    spec:
      fqdn: app.yoganova.my.id
      target: http://example-service.services.svc.cluster.local:80
tunnelRef:
  kind: ClusterTunnel
  name: homelab-tunnel-yoganova
```
