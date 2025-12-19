# GitOps Applications

This directory contains the Argo CD `Application` custom resources that drive the entire cluster's deployment.

## Structure

Each file here defines an application (or a group of applications) that Argo CD monitors:
- **`argocd.yml`**: Self-manages the Argo CD deployment.
- **`monitoring.yml`**: Manages the observability stack.
- **`services.yml`**: Manages application services.
- **`tools.yml`**: Manages general utilities and tools.
- And others for specific components like `harbor`, `immich`, `media`, etc.

## How it Works

The root `apps.yml` implements the **App-of-Apps** pattern, pointing Argo CD to this directory. Argo CD then recursively syncs all applications defined here.

### Manual Sync
```bash
argocd app sync apps
```
