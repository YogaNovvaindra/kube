# Trivy Operator

Trivy is a comprehensive security scanner for container images, file systems, and configuration issues.

## Components

- **`operator-deployment.yml`**: The Trivy operator that watches cluster resources.
- **`operator-config.yml`**: General configuration for the operator.
- **`trivy-config.yml`**: Custom scan settings.
- **`kustomization.yml`**: Orchestrates the Trivy deployment.

## Reports

Trivy automatically generates `VulnerabilityReports` and `ConfigAuditReports` for pods and other resources in the cluster.

### View Reports
```bash
kubectl get vulnerabilityreports -A
```
