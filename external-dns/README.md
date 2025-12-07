# ExternalDNS with Cloudflare Tunnel

This setup enables automatic DNS record management in Cloudflare using ExternalDNS, integrated with your existing Cloudflare tunnel. Define your public domains in Kubernetes YAML files instead of manually configuring them in the Cloudflare dashboard.

## Quick Start

1. **Create Cloudflare API Token** with Zone Read + DNS Edit permissions
2. **Create sealed secret**: `kubectl create secret generic external-dns-cred --from-literal=CF_API_TOKEN='YOUR_TOKEN' --namespace=external-dns --dry-run=client -o yaml | kubeseal -o yaml > services/external-dns/external-dns-cred.yml`
3. **Deploy cloudflared config**: `kubectl apply -f services/cloudflared-config.yml`
4. **Add to ArgoCD**: The gitops configuration is ready at `gitops/external-dns.yml`
5. **Add annotations** to your Services or Ingresses (see examples below)

## Architecture

Since you have no public IP, the setup works as follows:

1. **ExternalDNS**: Watches Kubernetes resources (Ingress, Services) and automatically creates DNS records in Cloudflare (proxied records)
2. **Cloudflare Tunnel**: Routes traffic directly to services:
   - `ygnv.my.id` (root only) → Ghost service
   - `*.yoganova.my.id` (all subdomains) → Various services (portfolio, etc.)
3. **No Traefik needed**: All routing is handled directly by Cloudflare Tunnel config

**Key Points**: 
- The cloudflared config file manages all routing - no need for Cloudflare dashboard or Traefik
- ExternalDNS manages: `ygnv.my.id` (root only) and `*.yoganova.my.id` (all subdomains)
- Simple and direct - each service gets its own route in the cloudflared config

## Setup Instructions

### 1. Create Cloudflare API Token

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use the "Edit zone DNS" template or create a custom token with:
   - **Zone**: Read permissions
   - **DNS**: Edit permissions
   - **Access**: All zones (or specific zones if restricting)

### 2. Create Sealed Secret

Create the sealed secret for ExternalDNS credentials:

```bash
kubectl create secret generic external-dns-cred \
  --from-literal=CF_API_TOKEN='YOUR_CLOUDFLARE_API_TOKEN' \
  --namespace=external-dns \
  --dry-run=client -o yaml | kubeseal -o yaml > services/external-dns/external-dns-cred.yml
```

Replace `YOUR_CLOUDFLARE_API_TOKEN` with your actual API token.

### 3. Deploy Cloudflared Configuration

The cloudflared config file (`services/cloudflared-config.yml`) routes traffic directly to services:
- `ygnv.my.id` (root only) → Ghost service
- `*.yoganova.my.id` (all subdomains) → Various services

**Important**: This config will override any routing you've configured in the Cloudflare dashboard. All routing is now managed via this config file - no Traefik needed.

Deploy the config:
```bash
kubectl apply -f services/cloudflared-config.yml
```

The config works with token-based authentication - the tunnel ID is automatically extracted from your `TUNNEL_TOKEN`.

### 4. Deploy ExternalDNS

ExternalDNS will be deployed via ArgoCD once you add it to gitops (see below).

## Usage

### Direct Service Routing (No Traefik)

All services route directly via Cloudflare Tunnel. For each service:

1. **Add ExternalDNS annotation to Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: services
  annotations:
    # For yoganova.my.id subdomains (e.g., myservice.yoganova.my.id)
    external-dns.alpha.kubernetes.io/hostname: myservice.yoganova.my.id
    external-dns.alpha.kubernetes.io/ttl: "120"
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "true"
spec:
  type: ClusterIP
  selector:
    app: my-service
  ports:
    - port: 80
      targetPort: 8080
```

2. **Add route in `services/cloudflared-config.yml`**:
```yaml
ingress:
  # Root domain (ygnv.my.id only)
  - hostname: "ygnv.my.id"
    service: http://ghost.services.svc.cluster.local:2368
  
  # Specific subdomains of yoganova.my.id (add before wildcard)
  - hostname: "myservice.yoganova.my.id"
    service: http://my-service.services.svc.cluster.local:80
  
  # Wildcard for all other yoganova.my.id subdomains
  - hostname: "*.yoganova.my.id"
    service: http://portfolio.services.svc.cluster.local:80
  
  # Catch-all (must be last)
  - service: http_status:404
```

**Note**: 
- `ygnv.my.id` (root only) is managed by ExternalDNS - add annotation to the service
- `*.yoganova.my.id` (all subdomains) are managed by ExternalDNS - add annotations to services
- Add specific routes in cloudflared-config.yml before the wildcard if you need different routing

See `services/external-dns/example.yml` for a complete example.

## Annotations Reference

- `external-dns.alpha.kubernetes.io/hostname`: The hostname(s) to create DNS records for (comma-separated for multiple)
- `external-dns.alpha.kubernetes.io/ttl`: TTL in seconds (120 or above, or 1 for automatic)
- `external-dns.alpha.kubernetes.io/cloudflare-proxied`: Set to "true" to enable Cloudflare proxy (DDOS protection, CDN)
- `external-dns.alpha.kubernetes.io/cloudflare-tags`: Comma-separated tags for DNS records (e.g., "env:prod,team:backend")

## How It Works

1. You create a Service with ExternalDNS annotations
2. ExternalDNS detects the annotation and creates a proxied DNS record in Cloudflare
3. The DNS record points to Cloudflare (proxied, so no public IP needed)
4. Cloudflare Tunnel receives the traffic and routes directly to services based on hostname matching in `cloudflared-config.yml`
5. No Traefik needed - direct routing from tunnel to services

**No Public IP Required**: The Cloudflare Tunnel handles all external connectivity and routes directly to your internal services. Simple and efficient!

## Troubleshooting

### Check ExternalDNS logs:
```bash
kubectl logs -n external-dns deployment/external-dns
```

### Verify DNS records in Cloudflare:
Check your [Cloudflare DNS dashboard](https://dash.cloudflare.com/) to see if records are being created.

### Check if ExternalDNS is watching resources:
```bash
kubectl get ingress -A -o yaml | grep external-dns
kubectl get svc -A -o yaml | grep external-dns
```

## Migrating from Dashboard-Based Routing

If you're currently managing tunnel routing in the Cloudflare dashboard (`one.dash.cloudflare.com`), this setup will replace that:

1. **Before**: Routes configured in Cloudflare dashboard → Individual services
2. **After**: Config file routes directly to services (no Traefik needed)

**Migration Steps**:
1. Deploy the `cloudflared-config.yml` - this will override dashboard routing
2. Add routes for each service in the cloudflared config file
3. Remove any individual routes from the Cloudflare dashboard (they're now handled by the config)
4. Add ExternalDNS annotations to services to create DNS records automatically

## Notes

- ExternalDNS manages:
  - `ygnv.my.id` (root domain only, no subdomains)
  - `*.yoganova.my.id` (all subdomains)
- Records are automatically removed when you delete the annotated resource
- Cloudflare proxy is enabled by default (can be disabled per-resource)
- All routing is defined in `cloudflared-config.yml` - direct to services, no Traefik
- No public IP needed - everything goes through Cloudflare Tunnel
- All routing is now defined in Kubernetes YAML, not in the Cloudflare dashboard

