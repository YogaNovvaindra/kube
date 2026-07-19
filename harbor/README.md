# 🐳 Harbor

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content.

## 📂 Structure

- **`values.yaml`**: Helm chart configuration values.
- **`values-full.yaml`**: Complete reference Helm chart values.
- **`config/`**: Directory containing Harbor configuration files and credentials.

## 🚀 Deployment

Harbor is deployed using the official Helm chart from `https://helm.goharbor.io`.

- **Source**: [gitops/harbor.yml](gitops/harbor.yml)
- **Configuration**: [values.yaml](harbor/values.yaml)

## ⚙️ Usage

Harbor is used to host custom images and proxy public registries to improve pull speeds and security.
