# 🏡 HomeLab Kubernetes Cluster

Welcome to my HomeLab Kubernetes Cluster! This repository contains the configuration and deployment files for managing various services and applications in my homelab environment. The cluster is designed to provide a self-hosted, automated, and scalable infrastructure for personal and experimental use.

## 📋 Table of Contents

- [Screenshots](#-screenshots)
- [Overview](#-overview)
- [Statistics](#-statistics)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Repository Structure](#-repository-structure)
- [Applications](#-applications)
  - [Core Infrastructure & GitOps](#-core-infrastructure--gitops)
  - [General Tools & Utilities](#️-general-tools--utilities)
  - [Observability & Monitoring](#-observability--monitoring)
  - [Application Services](#-application-services)
  - [Media](#-media)
- [Infrastructure](#-infrastructure)
- [Deployment Workflow](#-deployment-workflow)
- [Security Implementation](#-security-implementation)
- [Troubleshooting](#-troubleshooting)
- [Contributing & Adaptation](#-contributing--adaptation)
- [License](#-license)

## 📸 Screenshots

### 🏠 Homepage

![Homepage](images/homepage.png)

### 🚀 ArgoCD

![ArgoCD](images/argocd.png)

### 📊 Grafana

![Grafana](images/grafana.png)

## 📊 Statistics

- **Total Applications**: 60+ services across 15+ namespaces
- **Storage Solutions**: CephFS (distributed) + RustFS (S3-compatible)
- **Monitoring Stack**: Full observability with 13+ exporters and Prometheus/Grafana/Tempo/Loki
- **Security Tools**: Sealed Secrets, Trivy, Authentik SSO, Network Policies
- **Automation**: GitOps with ArgoCD, Keel for auto-updates, Renovate for dependency management

## 🌟 Overview

The Kubernetes cluster follows **declarative infrastructure management** principles, where all configurations are version-controlled and automatically synchronized with the cluster state. Key organizational components include:

- **📁 Namespace Segregation**: Services are grouped by purpose, often residing in dedicated namespaces named after the application or service group (e.g., `harbor`, `monitoring`).
- **⚙ GitOps Workflow**: ArgoCD-driven continuous deployment from Git repository
- **🔐 Security First**: Sealed Secrets for encrypted credential management
- **🤖 Automated Updates**: Keel for container images and Renovate for dependency versions

## 🚀 Features

- **📜 Declarative Configuration**: Entire infrastructure defined as code in version-controlled manifests
- **🔄 GitOps Automation**: ArgoCD synchronization with self-healing capabilities
- **🆕 Continuous Updates**:
  - `Keel`: Automatic rolling updates for latest container images
  - `Renovate`: Semantic versioning maintenance for container images
- **📊 Observability Stack**: Prometheus/Grafana metrics, Loki logs, and Tempo tracing with alert integration
- **🗄 Persistent Storage**: CephFS provisioner with automated volume management, plus RustFS for S3-compatible object storage
- **🔒 Zero-Trust Security**: Authentik SSO integration and network policies
- **📡 Load Balancing**: MetalLB for bare-metal load balancing
- **🛡️ Secure Tunnels**: Cloudflare Operator for zero-trust tunnel routing

## 📋 Prerequisites

Before deploying this infrastructure, ensure you have:

- **Kubernetes Cluster**: MicroK8s or compatible Kubernetes distribution (v1.24+)
- **Storage**: CephFS provisioner configured or alternative storage class
- **Network**:
  - MetalLB configured for LoadBalancer services (bare-metal)
  - DNS configured for ingress domains
  - Optional: Cloudflare tunnel for external access
- **Git Repository**: Access to this repository for ArgoCD
- **Sealed Secrets**: Sealed Secrets controller installed and configured
- **Container Registry**: Access to container images (Harbor or public registries)
- **Hardware**:
  - Sufficient resources for 60+ applications
  - GPU support for media transcoding (Intel QuickSync supported)
  - Network-attached storage for persistent volumes

## 🚀 Quick Start

1. **Bootstrap ArgoCD**:

   ```bash
   kubectl apply -f argocd/
   ```

2. **Deploy App-of-Apps**:

   ```bash
   kubectl apply -f apps.yml
   ```

3. **Access ArgoCD UI**:

   - Port-forward: `kubectl port-forward svc/argocd-server -n argocd 8080:443`
   - Get admin password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

4. **Monitor Deployments**:

   - ArgoCD will automatically sync applications from the `gitops/` directory
   - Check status in ArgoCD UI or via CLI: `argocd app list`

5. **Configure Sealed Secrets**:
   - Install Sealed Secrets controller if not already installed
   - Seal your secrets using `kubeseal` before committing

> **Note**: Some applications require manual configuration of secrets and ingress rules. Refer to individual application directories for specific setup instructions.

## 📂 Repository Structure

This Git repository is organized to support a GitOps workflow with ArgoCD:

- **`gitops/`**: GitOps orchestration directory containing ArgoCD `Application` definitions. These resources manage the lifecycle of all cluster applications, including core infrastructure and user services.
- **`apps.yml`**: Implementation of the "App-of-Apps" pattern, serving as the root entry point for ArgoCD to manage the `gitops/` directory.
- **Application Manifests**: Top-level directories (e.g., `harbor/`, `monitoring/`, `services/`) containing raw Kubernetes manifests, Kustomize overlays, or Helm chart `values.yaml` files.
- **`cluster/`**: Contains core system-level services consolidated into the cluster-wide GitOps management flow.

## 📦 Applications

This cluster hosts a variety of self-managed applications and services.

### 🚀 Core Infrastructure & GitOps

- **🔄 ArgoCD**: GitOps deployment controller.
- **🐋 Keel**: Automated image updates for latest tags (located in [cluster.yml](./gitops/cluster.yml)).
- **[🕵️ Portainer Agent](./portainer/portainer-agent.yml)**: Connects to a Portainer instance for cluster management.
- **🔏 Sealed Secrets**: Manages encrypted secrets in Git (located in [cluster.yml](./gitops/cluster.yml)).
- **♻️ Reloader**: Automatically restarts pods when ConfigMaps or Secrets are updated (located in [cluster.yml](./gitops/cluster.yml)).
- **🚦 Traefik**: TLS-terminating ingress controller (mentioned in Infrastructure).
- **⚖️ MetalLB**: Load balancer for bare-metal environments (mentioned in Infrastructure).

### 🛠️ General Tools & Utilities

#### 🔐 Security & Authentication

- [🔑 Authentik](./tools/authentik): Centralized authentication and identity provider.
- [🛡️ Vaultwarden](./tools/security/vaultwarden.yml): Self-hosted password manager (Bitwarden compatible).

#### 💻 Development & Code Management

- [💻 Gitea](./tools/git/gitea.yml): Self-hosted Git service and repository manager.
- [📚 Outline](./tools/editor/outline.yml): Collaborative knowledge base/wiki.
- [⚙️ Semaphore](./tools/cluster/semaphore.yml): UI for running Ansible playbooks.

#### 📝 Document & File Management

- [📄 BentoPDF](./tools/editor/bentopdf.yml): Self-hosted PDF manipulation and conversion tool suite.
- [📂 FileBrowser](./tools/storage/filebrowser.yml): Web-based file management interface for remote access.
- [📁 Samba](./tools/storage/samba.yml): SMB/CIFS file sharing server for native network mounts.
- [🔗 Syncthing](./tools/cluster/syncthing.yml): Continuous file synchronization across devices.

#### 🗄️ Storage & Databases

- [🗄️ RustFS](./tools/storage/rustfs.yml): S3-compatible object storage solution.
- [🐘 pgAdmin](./db/pgadmin.yml): PostgreSQL administration and development platform.
- [🐬 phpMyAdmin](./db/phpmyadmin.yml): Web-based administration tool for MySQL and MariaDB.

#### 🎨 Collaboration & Productivity

- [🎨 Excalidraw](./tools/editor/excalidraw.yml): Virtual collaborative whiteboard.
- [🏠 Homepage](./tools/homepage): Dashboard for managing and accessing all services.
- [🔄 n8n](./tools/automation/n8n.yml): Workflow automation platform.
- [🏡 Home Assistant](./tools/automation/homeassistant.yml): Open-source home automation platform.
- [🔌 ESPHome](./tools/automation/esphome.yml): Management for ESP boards.
- [🔍 Changedetection.io](./tools/automation/changedetection.yml): Self-hosted website change monitoring.
- [🔧 IT-Tools](./tools/utilities/it-tools.yml): Collection of handy online tools for developers.
- [🌐 Netbird](./tools/cluster/netbird.yml): Mesh VPN and P2P networking solution for secure access.
- [💨 Speedtest](./tools/network/speedtest.yml): Tool for checking internet connection speed.
- [🛡️ Vert](./tools/editor/vert.yml): Clean and simple RSS feed reader.
- [📦 Warrior](./tools/archiving/warrior.yml): Archive Team Warrior for distributed archiving.

### 📊 Observability & Monitoring

- [🛡️ AdGuard Exporter](./monitoring/adguard-exporter.yml): Exports AdGuard DNS metrics to Prometheus.
- [📜 Fluent-bit](./monitoring/fluent-bit.yml): Dual setup for processing and forwarding container logs and Kubernetes events.
- [📊 Grafana](./monitoring/grafana/grafana.yml): Dashboards for visualizing metrics and logs, powered by image renderer sidecar.
- [☸️ Kube State Metrics](./monitoring/kube-state-metrics.yml): Exposes cluster-level metrics.
- [✍️ Loki](./monitoring/loki-deploy.yml): Horizontally-scalable, multi-tenant log aggregation system.
- [📡 MKTXP](./monitoring/mktxp.yml): Exporter for MikroTik router metrics.
- [💻 Node Exporter](./monitoring/node-exporter.yml): Hardware and OS metrics exporter for *NIX kernels.
- [📈 Prometheus](./monitoring/prometheus/prometheus-deploy.yml): Metrics collection and alerting toolkit.
- [🖥️ PVE Exporter](./monitoring/pve-exporter.yml): Exporter for Proxmox VE host and guest metrics.
- [📡 SNMP Exporter](./monitoring/snmp-exporter.yml): Exporter for metrics from SNMP-enabled devices.
- [🕵️ Tempo](./monitoring/tempo.yml): Horizontally-scalable, multi-tenant distributed tracing system.
- [💓 Uptime Kuma](./monitoring/uptime/uptime-kuma.yml): Self-hosted uptime monitoring tool.

### 📦 Application Services

- [🐳 Harbor](./harbor/): Enterprise-grade cloud native container registry.
- [🖼️ Immich](./immich/immich.yml): Self-hosted high-performance photo and video backup solution.
- [💰 Money](./money/money.yml): Personal finance management and budgeting application.
- [🗄️ DB Backup](./services/db-backup/db-backup.yml): Automated multi-database backup cronjob.
- [☁️ Cloudflare Operator](./cloudflare-operator): Kubernetes native controller for zero-trust Cloudflare Tunnels.
- [🌿 EcoGuardian](./services/ecoguardian/ecoguardian.yml): Environmental monitoring and analytical service.
- [✍️ Ghost](./services/ghost/ghost.yml): Professional self-hosted publishing platform and blog.
- [📊 Linear Next](./services/linear-next/linear-next.yml): Streamlined issue tracking and project management suite.
- [🐘 Tolonto](./services/tolonto/tolonto.yml): PHP LAMP development stack.
- [🖼️ Portfolio](./services/portfolio/portfolio.yml): Personal showcase application with auto-scaling capabilities.

### 🎬 Media

- [🎬 Plex Media Server](./media/player.yml): 4K hardware transcoding capable media server.
- [🎬 Jellyfin](./media/player.yml): Open-source alternative media server.
- [📺 Arr Suite](./media): Radarr, Sonarr, Bazarr, Prowlarr stack for automated media management.
- [📥 Transmission](./media/download.yml): Torrent client powered by Flood UI.
- [📥 qBittorrent & Qui](./media/qbittorrent.yml): Feature-rich torrent client with multi-instance Web UI.
- [📊 Tautulli](./media/tautulli.yml): Plex usage monitoring and analytics.
- [📂 Seerr](./media/seerr.yml): Media request management and discovery.
- [🧹 Maintainerr](./media/maintainerr.yml): Rule-based automated media library cleanup.
- [🔄 Crosswatch](./media/crosswatch.yml): Media watch progress synchronization across platforms.
- [🔧 FlareSolverr](./media/flaresolverr.yml): Proxy server to bypass Cloudflare protection for indexers.

## 🛠 Infrastructure

### Core Platform

- **☸ Kubernetes**: MicroK8s cluster with embedded Ceph storage
- **📦 Helm**: Package manager for chart deployments
- **🏷️ Node Feature Discovery (NFD)**: Detects hardware features and labels nodes, enabling advanced workload scheduling

### Networking & Ingress

- **🚦 Traefik**: TLS-terminating ingress controller with automatic Let's Encrypt certificates.
- **📡 MetalLB**: Load balancer for bare-metal environments providing internal IP management.
- **🌐 Netbird**: VPN mesh networking for secure remote access.
- **☁️ Cloudflare Operator**: Secure Cloudflare Tunnel CRDs for exposing services without public IPs or port forwarding.

### Storage

- **🗂 CephFS**: Distributed storage with replication (primary storage)
- **🗄️ RustFS**: S3-compatible object storage for applications requiring S3 API

### Security & Certificates

- [🔐 Authentik](./tools/authentik): Centralized authentication gateway and SSO provider.
- [🔒 cert-manager](./cert-manager): Automated TLS certificate management with Let's Encrypt integration.
- [🛡️ Trivy](./trivy): Container vulnerability scanning and security analysis.

### Data & Caching

- **💾 Valkey/Redis**: In-memory data store used by Authentik, Immich, and other services
- **🗄️ PostgreSQL/MariaDB**: Relational databases for various applications

## 📜 Deployment Workflow

The cluster follows a GitOps workflow where all changes are driven through Git commits:

```mermaid
graph TB
    A[Developer: Git Commit] --> B[GitHub Repository]
    B --> C[ArgoCD Detects Changes]
    C --> D[ArgoCD Syncs Manifests]
    D --> E{Kubernetes Cluster}
    E --> F[Application Deployment]
    F --> G[Keel Monitors Images]
    G --> H[Renovate Checks Dependencies]
    H --> I{Updates Available?}
    I -->|Yes| J[Create PR or Auto-merge]
    J --> A
    I -->|No| K[Monitor & Maintain]
    K --> G
```

### Workflow Components

1. **Git Commit**: All infrastructure changes are committed to this repository
2. **ArgoCD Sync**: ArgoCD continuously monitors the repository and syncs changes
3. **Application Deployment**: Kubernetes resources are created/updated automatically
4. **Keel Monitoring**: Keel watches container registries for new image tags
5. **Renovate**: Automatically creates PRs for dependency updates
6. **Self-Healing**: ArgoCD automatically corrects drift from desired state

## 🔒 Security Implementation

- **🔏 Sealed Secrets**: Encrypted secrets using cluster-specific certificates
- **🛡️ Trivy**: Vulnerability scanning for container images and other artifacts
- **🔐 RBAC Enforcement**: Namespace-bound service accounts
- **🛡 Network Policies**: Zero-trust pod communication rules
- **🔒 Vaultwarden**: Self-hosted Bitwarden-compatible secrets manager

## 🔧 Troubleshooting

### Common Issues

#### ArgoCD Applications Not Syncing

```bash
# Check application status
argocd app list

# Get detailed status
argocd app get <app-name>

# Force sync if needed
argocd app sync <app-name>
```

#### Pods Stuck in Pending

- Check node resources: `kubectl describe node`
- Verify storage classes: `kubectl get storageclass`
- Check node selectors match available nodes

#### Storage Issues

- Verify CephFS is mounted: `kubectl get pv`
- Check storage class: `kubectl get storageclass`
- Review PVC status: `kubectl get pvc -A`

#### Certificate/Ingress Issues

- Verify cert-manager is running: `kubectl get pods -n cert-manager`
- Check certificate status: `kubectl get certificates -A`
- Review Traefik logs: `kubectl logs -n traefik -l app.kubernetes.io/name=traefik`

#### Secret Decryption Issues

- Ensure Sealed Secrets controller is running
- Verify secret was sealed with correct controller certificate
- Check sealed secret status: `kubectl get sealedsecrets -A`

### Useful Commands

```bash
# View all applications in ArgoCD
argocd app list

# Check resource usage
kubectl top nodes
kubectl top pods -A

# View logs for a specific service
kubectl logs -n <namespace> <pod-name>

# Describe a resource for debugging
kubectl describe pod -n <namespace> <pod-name>
```

### Getting Help

- Check ArgoCD UI for application sync status and errors
- Review Grafana dashboards for resource metrics
- Check Prometheus alerts for system issues
- Review individual application logs in their respective namespaces

## 🤝 Contributing & Adaptation

While primarily personal infrastructure, this setup demonstrates:

- Enterprise-grade patterns for homelab use
- Scalable GitOps implementation
- Security-conscious home infrastructure
  Feel free to fork and adapt components to your environment!

## 📜 License

This project is licensed under the MIT License.
