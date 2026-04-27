# Cloudflare Operator Integration

This directory contains the configuration for the [adyanth/cloudflare-operator](https://github.com/adyanth/cloudflare-operator).

## Setup Instructions

### 1. Cloudflare API Token

> [!IMPORTANT] > **Required API Token Permissions**
>
> Valid Cloudflare API Token permissions are required for the operator to function:
>
> - `Account > Cloudflare Tunnel > Edit`
> - `Account > Account Settings > Read`
> - `Zone > DNS > Edit`

Then seal it into `cloudflare-secret.yml`:

```bash
# Replace YOUR_TOKEN with actual token
echo -n "YOUR_TOKEN" | kubeseal --raw --scope cluster-wide --name cloudflare-cred --namespace cloudflare-operator-system
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

> [!WARNING]
> **First deployment requires two-step apply.** The operator CRDs must be registered before `ClusterTunnel` resources can be created. Also, the `SealedSecret` must be unsealed into a regular `Secret` before the operator can authenticate to Cloudflare.

**First-time deployment:**

```bash
# Step 1: Deploy operator + SealedSecret only (CRDs need to register first)
kubectl apply -k https://github.com/adyanth/cloudflare-operator/config/default?ref=v0.13.1
kubectl apply -f cloudflare-cred.yml

# Step 2: Wait for operator to be ready and secret to be unsealed
kubectl wait --for=condition=available deploy/cloudflare-operator-controller-manager \
  -n cloudflare-operator-system --timeout=120s
kubectl get secret cloudflare-cred -n cloudflare-operator-system  # verify it exists

# Step 3: Now apply the ClusterTunnel resources
kubectl apply -f cluster-tunnel-ygnv.yml
kubectl apply -f cluster-tunnel-yoganova.yml
```

**Subsequent deploys** (operator is already running):

ArgoCD will pick up the changes once committed, or you can apply manually:

```bash
kubectl apply -k .
```

### 4. Migration

Once verified, remove the old manual cloudflared deployment in `services/cloudflared.yml`.

---

## Troubleshooting

### FailedMount: secret "homelab-tunnel-xxx" not found

```
MountVolume.SetUp failed for volume "creds" : secret "homelab-tunnel-xxx" not found
```

**Cause:** The operator creates a tunnel in Cloudflare and stores its credentials in a Kubernetes Secret with the same name as the tunnel. If that secret is lost (e.g. namespace was deleted/recreated, or the operator crashed during initial setup), the operator enters a broken state with `"empty tunnel creds"` and cannot recover on its own.

**Fix — delete and recreate the tunnels:**

```bash
# 1. Delete the broken ClusterTunnel resources
kubectl delete clustertunnel homelab-tunnel-ygnv
kubectl delete clustertunnel homelab-tunnel-yoganova

# 2. Clean up stale Cloudflare tunnels
#    Go to Cloudflare Dashboard → Zero Trust → Networks → Tunnels
#    Delete any leftover tunnels with matching names if they still exist

# 3. Clean up leftover K8s resources
kubectl delete deploy,configmap,secret homelab-tunnel-ygnv homelab-tunnel-yoganova \
  -n cloudflare-operator-system --ignore-not-found

# 4. Re-apply the ClusterTunnel resources
kubectl apply -f cluster-tunnel-ygnv.yml
kubectl apply -f cluster-tunnel-yoganova.yml
```

> [!TIP]
> After re-applying, verify the secrets were created:
> ```bash
> kubectl get secret -n cloudflare-operator-system | grep homelab-tunnel
> ```
> You should see a secret for each tunnel. If not, check operator logs:
> ```bash
> kubectl logs deploy/cloudflare-operator-controller-manager \
>   -n cloudflare-operator-system --tail=50
> ```
