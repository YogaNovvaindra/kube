# Cloudflare Operator Integration

This directory contains the configuration for the [adyanth/cloudflare-operator](https://github.com/adyanth/cloudflare-operator).

## Setup Instructions

### 1. Cloudflare API Token

You need a Create an API Token in Cloudflare Dashboard:

- `Account > Cloudflare Tunnel > Edit`
- `Account > Account Settings > Read`
- `Zone > DNS > Edit`

Then seal it into `cloudflare-secret.yml`:

```bash
# Replace YOUR_TOKEN with actual token
echo -n "YOUR_TOKEN" | kubeseal --raw --scope cluster-wide --name cloudflare-cred --namespace cloudflare-operator
```

Replace the value in `cloudflare-secret.yml`.

### 2. Configure Tunnel

Update `cluster-tunnel.yml` with your Cloudflare Account ID.

Note: `accountId` must be in the YAML file as it is required by the operator schema and cannot be read from the secret for this resource type.

**How to find Cloudflare Account ID:**

1. Log in to the Cloudflare Dashboard.
2. Select your domain.
3. On the "Overview" page, scroll down to the right sidebar.
4. Copy the "Account ID" (it's a 32-character hex string).

### 3. Deploy

ArgoCD will pick up the changes once committed, or you can apply manually:

```bash
kubectl apply -k .
```

### 4. Migration

Once verified, remove the old manual cloudflared deployment in `services/cloudflared.yml`.
