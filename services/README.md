# 🚀 Application Services

This directory contains various personal and application services running in the cluster.

## 📂 Structure

- **`ghost/`**: Professional publishing platform and blog.
- **`portfolio/`**: Personal project showcase (Auto-scales via HPA).
- **`linear-next/`**: Issue tracking and project management.
- **`ecoguardian/`**: Environmental monitoring service.
- **`tolonto/`**: PHP LAMP development stack.
- **`db-backup/`**: Generic, automated multi-database backup CronJob configuration (backs up MySQL, PostgreSQL).
- **`discord/`**: Shared Discord webhook credentials for service alerts.

## ⚙️ Configuration (Cloudflare Tunnel Routing)

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
