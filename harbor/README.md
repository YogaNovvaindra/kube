# Harbor

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content.

## Deployment

Harbor is deployed using the official Helm chart from `https://helm.goharbor.io`.

- **Source**: [gitops/harbor.yml](file:///home/yoga/Documents/kube/gitops/harbor.yml)
- **Configuration**: [values.yaml](file:///home/yoga/Documents/kube/harbor/values.yaml)

## Usage

Harbor is used to host custom images and proxy public registries to improve pull speeds and security.
