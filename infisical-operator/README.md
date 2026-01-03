# Infisical Secret Operator

Kubernetes operator that syncs secrets from the off-cluster Infisical instance.

## Prerequisites

1. Infisical running (see [../infisical/](../infisical/))
2. Machine Identity created in Infisical with Universal Auth

## Setup

### 1. Create Machine Identity in Infisical

1. Go to Infisical UI → Project Settings → Machine Identities
2. Create new identity with Universal Auth
3. Copy the Client ID and Client Secret

### 2. Create Credentials Secret

```bash
# Create sealed secret for credentials
kubectl create secret generic universal-auth-credentials \
  --namespace=default \
  --from-literal=clientId=YOUR_CLIENT_ID \
  --from-literal=clientSecret=YOUR_CLIENT_SECRET \
  --dry-run=client -o yaml | kubeseal -o yaml > credentials-sealed.yaml

kubectl apply -f credentials-sealed.yaml
```

### 3. Deploy via ArgoCD

The operator is deployed via `gitops/infisical-operator.yml`.

## Usage

Create an `InfisicalSecret` to sync secrets:

```yaml
apiVersion: secrets.infisical.com/v1alpha1
kind: InfisicalSecret
metadata:
  name: my-app-secrets
  namespace: default
spec:
  hostAPI: https://infisical.yourdomain.com # Your Infisical URL
  resyncInterval: 60 # seconds
  authentication:
    universalAuth:
      secretsScope:
        projectSlug: my-project
        envSlug: prod
        secretsPath: "/"
      credentialsRef:
        secretName: universal-auth-credentials
        secretNamespace: default
  managedSecretReference:
    secretName: my-app-secrets-synced
    secretNamespace: default
```
