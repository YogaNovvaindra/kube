# Discord Notifications for ArgoCD

This guide explains how to set up Discord notifications for ArgoCD application events.

## Prerequisites

- ArgoCD installed in your cluster
- Discord server with webhook access
- `kubeseal` CLI tool installed

## Setup Instructions

### 1. Create Discord Webhook

1. Go to your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Configure the webhook:
   - Set a name (e.g., "ArgoCD Notifications")
   - Choose the channel for notifications
   - Copy the webhook URL

### 2. Create and Seal the Secret

Replace the placeholder with your actual Discord webhook URL:

```bash
# Edit the secret file
nano discord-webhook-secret.yaml

# Replace YOUR_DISCORD_WEBHOOK_URL_HERE with your actual webhook URL
# Example: https://discord.com/api/webhooks/123456789/abcdefghijklmnop

# Seal the secret using kubeseal
kubeseal --format=yaml < discord-webhook-secret.yaml > discord-webhook-sealed-secret.yaml

# Delete the unsealed secret file (IMPORTANT for security)
rm discord-webhook-secret.yaml

# Commit the sealed secret
git add discord-webhook-sealed-secret.yaml
git commit -m "Add Discord webhook sealed secret for ArgoCD notifications"
```

### 3. Apply Configuration

The configuration is already included in the kustomization. Apply it:

```bash
kubectl apply -k .
```

### 4. Enable Notifications on Applications

Add annotations to your ArgoCD Application resources to enable notifications:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  annotations:
    # Enable all notification triggers
    notifications.argoproj.io/subscribe.on-sync-succeeded.discord: ""
    notifications.argoproj.io/subscribe.on-sync-failed.discord: ""
    notifications.argoproj.io/subscribe.on-health-degraded.discord: ""
    notifications.argoproj.io/subscribe.on-sync-running.discord: ""
spec:
  # ... your app spec
```

Or enable specific notifications only:

```yaml
metadata:
  annotations:
    # Only notify on failures and degraded health
    notifications.argoproj.io/subscribe.on-sync-failed.discord: ""
    notifications.argoproj.io/subscribe.on-health-degraded.discord: ""
```

## Available Notification Triggers

| Trigger | Description | When Sent |
|---------|-------------|-----------|
| `on-sync-succeeded` | ✅ Sync completed successfully | App sync phase is `Succeeded` |
| `on-sync-failed` | ❌ Sync failed | App sync phase is `Error` or `Failed` |
| `on-health-degraded` | ⚠️ App health degraded | App health status is `Degraded` |
| `on-sync-running` | 🔄 Sync started | App sync phase is `Running` |

## Notification Content

Each notification includes:
- **Application name**
- **Sync status**
- **Health status**
- **Git revision** (for successful syncs)
- **Error message** (for failed syncs)
- **Timestamp**
- **Color-coded embeds** (green for success, red for failure, yellow for warnings)

## Troubleshooting

### Notifications not appearing

1. Check the notifications controller logs:
   ```bash
   kubectl logs -n argocd -l app.kubernetes.io/name=argocd-notifications-controller
   ```

2. Verify the secret exists:
   ```bash
   kubectl get secret -n argocd argocd-notifications-secret
   ```

3. Verify the ConfigMap:
   ```bash
   kubectl get configmap -n argocd argocd-notifications-cm
   ```

4. Check Application annotations:
   ```bash
   kubectl get application -n argocd <app-name> -o yaml | grep notifications
   ```

### Testing notifications

Trigger a manual sync to test:
```bash
argocd app sync <app-name>
```

## Customization

To customize notification templates, edit `patches/configmap-notifications.yaml` and modify the Discord embed format. You can change:
- Colors (decimal color codes)
- Fields displayed
- Message format
- Avatar and username

Refer to [Discord Webhook Documentation](https://discord.com/developers/docs/resources/webhook) for embed formatting options.
