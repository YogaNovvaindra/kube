# Cert-Manager

This directory handles the automated management and issuance of TLS certificates from various issuing sources, including Let's Encrypt.

## Components

- **`cluster-issuer.yml`**: Defines the `ClusterIssuer` for Let's Encrypt using HTTP01 or DNS01 challenges.
- **`cloudflare-secret.yml`**: Sealed secret containing the Cloudflare API token for DNS01 challenges.
- **`kustomization.yml`**: Orchestrates the deployment of cert-manager resources.

## Usage

Cert-manager is used by Ingress controllers (like Traefik) to automatically provision certificates when an `Ingress` or `IngressRoute` is created with specific annotations.

### Verification
Check the status of certificates:
```bash
kubectl get certificates -A
kubectl get clusterissuers
```
