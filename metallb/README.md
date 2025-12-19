# MetalLB

MetalLB provides a network load-balancer implementation for bare metal Kubernetes clusters, using standard routing protocols.

## Components

- **`metallb-config.yml`**: Defines the IP address pools and L2 advertisement configuration for the cluster.
- **`kustomization.yml`**: Manages the deployment of the configuration.

## IP Address Management

The configuration defines a range of IP addresses (from the local network) that MetalLB can assign to `Services` of type `LoadBalancer`.

### Check IP Status
```bash
kubectl get svc -A | grep LoadBalancer
```
