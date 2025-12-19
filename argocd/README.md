# Argo CD Deployment

This directory contains a Kustomize-based deployment of Argo CD using the official installation manifest as a remote base with custom overlays.

## Structure

```
argocd/
├── kustomization.yml              # Main kustomization file
├── ingress.yml                     # Traefik IngressRoute
└── patches/
    ├── configmap-cmd-params.yml   # Server insecure mode for Traefik
    ├── configmap-cm.yml           # Homepage account configuration
    ├── configmap-rbac.yml         # RBAC for homepage account
    ├── image-pull-policy.yml      # Set imagePullPolicy to IfNotPresent
    └── resources.yml              # Memory resource requests
```

## Customizations

- **Base**: Official Argo CD install.yaml from GitHub
- **Namespace**: `argocd`
- **Images**: All images pulled from `reg.ygnv.my.id` registry with explicit tags for Renovate
  - Argo CD: `reg.ygnv.my.id/quay/argoproj/argocd:v3.4.0`
  - Dex: `reg.ygnv.my.id/ghcr/dexidp/dex:v2.44.0`
  - Redis: `reg.ygnv.my.id/docker/redis:8.4.0-alpine`
- **Image Pull Policy**: `IfNotPresent` for all containers
- **Resource Requests**: 
  - Most containers: `memory: 64Mi`
  - Redis: `memory: 16Mi`
- **Server Mode**: Insecure (for Traefik ingress)
- **Accounts**: Homepage service account with readonly role
- **Ingress**: Traefik IngressRoute at `argocd.ygnv.my.id`

## Notifications

Argo CD is configured to send notifications to Discord using the `argocd-notifications-controller`.

### 1. Setup Discord Webhook
1. Create a webhook in your Discord channel and copy the URL.
2. Store the URL in a sealed secret:
   ```bash
   # Create a temporary secret file (do not commit)
   echo -n "https://discord.com/api/webhooks/..." > discord-webhook.url
   kubectl create secret generic argocd-notifications-secret --from-file=discord-webhook=discord-webhook.url --dry-run=client -o yaml | kubeseal > discord-webhook-sealed-secret.yml
   rm discord-webhook.url
   ```

### 2. Enable Notifications
Add annotations to your `Application` resources:
```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.discord: ""
    notifications.argoproj.io/subscribe.on-sync-failed.discord: ""
```

---

## Deployment

### Build and preview
```bash
kubectl kustomize .
```

### Apply to cluster
```bash
kubectl apply -k . --server-side --force-conflicts
```

## Useful Commands

### Get initial admin password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Check Logs
```bash
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-notifications-controller
```
```