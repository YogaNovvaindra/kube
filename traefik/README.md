# Traefik Ingress Controller

Traefik is the edge router for this cluster, handling TLS termination and routing for all incoming traffic.

## CRD Maintenance

It is important to refresh the Traefik CRDs during minor updates to ensure compatibility with your current Traefik version.

### Official CRD Source
Check the version in the URL matches your Traefik deployment:
`https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml`

## IngressRoute Usage

All applications should use the `IngressRoute` CRD for advanced routing and TLS management. Refer to individual app manifests for examples.