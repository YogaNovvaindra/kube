# Argo CD Deployment

This directory contains a Kustomize-based deployment of Argo CD using the official installation manifest as a remote base with custom overlays.

## Structure

```
argocd/
├── kustomization.yaml              # Main kustomization file
├── ingress.yml                     # Traefik IngressRoute
└── patches/
    ├── configmap-cmd-params.yaml   # Server insecure mode for Traefik
    ├── configmap-cm.yaml           # Homepage account configuration
    ├── configmap-rbac.yaml         # RBAC for homepage account
    ├── image-pull-policy.yaml      # Set imagePullPolicy to IfNotPresent
    └── resources.yaml              # Memory resource requests
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

## Deployment

### Build and preview
```bash
kubectl kustomize /home/yoga/Documents/kube/argocd
```

### Apply to cluster

**Important**: Use server-side apply to handle large CRD annotations:
```bash
kubectl apply -k /home/yoga/Documents/kube/argocd --server-side --force-conflicts
```

Or from the argocd directory:
```bash
kubectl apply -k . --server-side --force-conflicts
```

### Delete deployment
```bash
kubectl delete -k /home/yoga/Documents/kube/argocd
```

## GitOps Management

When you add this to your `gitops/argocd.yml` as an Argo CD Application, it will:
- ✅ Automatically track updates from the official Argo CD GitHub repository
- ✅ Update CRDs and resources when the base manifest changes
- ✅ Apply your custom patches on top of the latest version
- ✅ Keep your deployment in sync with your Git repository

This means you get automatic updates to Argo CD while maintaining your customizations!

## Renovate Integration

✅ **Renovate will automatically update image tags** in `kustomization.yaml`:
- Detects `newTag` fields for all three images
- Creates PRs when new versions are available in your registry
- Keeps Argo CD, Dex, and Redis up-to-date

Make sure your `renovate.json` includes kustomize support (it should by default).

## Initial Admin Password

Get the initial admin password:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Updating

### Automatic Updates (via GitOps)
When managed by Argo CD, updates happen automatically as the official manifest changes on GitHub.

### Manual Updates
To update immediately:
```bash
kubectl apply -k . --server-side --force-conflicts
```

To pin to a specific version, add `newTag` to the images in `kustomization.yaml`.
```