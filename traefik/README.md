# 🚦 Traefik Ingress Controller

Traefik is the edge router for this cluster, handling TLS termination and routing for all incoming traffic.

## 📂 Structure

- **`traefik.yml`**: Main Traefik deployment and service.
- **`config.yml`**: Static and dynamic configuration parameters.
- **`kustomization.yml`**: Kustomize entrypoint for deployment.
- **`certificate.yml`**, **`tls-store.yml`**: TLS configuration resources.
- **`service-account.yml`**: RBAC permissions for Traefik.
- **`ingress.yml`**: Entrypoint routing for the Traefik dashboard.

## ⚙️ CRD Maintenance

It is important to refresh the Traefik CRDs during minor updates to ensure compatibility with your current Traefik version.

### Official CRD Source
Check the version in the URL matches your Traefik deployment:
`https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml`

## 🚀 IngressRoute Usage

All applications should use the `IngressRoute` CRD for advanced routing and TLS management. Refer to individual app manifests for examples.