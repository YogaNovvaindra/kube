# 🏡 HomeLab Kubernetes Cluster

Welcome to my HomeLab Kubernetes Cluster! This repository contains the configuration and deployment files for managing various services and applications in my homelab environment. The cluster is designed to provide a self-hosted, automated, and scalable infrastructure for personal and experimental use.

## 📸 Screenshots

### 🏠 Homepage
![Homepage](images/homepage.png)

### 🚀 ArgoCD
![ArgoCD](images/argocd.png)

### 📊 Grafana
![Grafana](images/grafana.png)

## 🌟 Overview

The Kubernetes cluster is organized into multiple namespaces, each dedicated to a specific category of services. These namespaces include:

- **🛠 Tools**: Utility applications for file management, monitoring, and automation.
- **📊 Monitoring**: Tools for metrics collection, visualization, and alerting.
- **🎥 Media**: Applications for managing and streaming media content.
- **💰 Money**: Services for passive income generation.
- **📸 Immich**: A self-hosted photo and video backup solution.
- **🏠 Homepage**: A dashboard for managing and monitoring the homelab.

## 🚀 Features

- **🔄 GitOps Workflow**: Managed using ArgoCD for continuous delivery and automated synchronization of applications.
- **🔒 Sealed Secrets**: Securely manage sensitive data using Bitnami's Sealed Secrets.
- **📈 Monitoring and Analytics**: Includes Prometheus, Grafana, and Node Exporter for real-time metrics and visualization.
- **🎞 Media Management**: Tools like Plex, Radarr, and Sonarr for media automation and streaming.
- **🔗 File Synchronization**: Syncthing for syncing files across devices.
- **🛡 Security**: Vaultwarden for password management and Authentik for identity and access management.
- **🤖 Automation**: Semaphore for Ansible automation and Keel for container image updates.

## 📦 Applications

### 🛠 Tools
- **📂 FileBrowser**: Web-based file management interface.
- **🔗 Syncthing**: File synchronization across devices.
- **🔒 Vaultwarden**: Self-hosted password manager.
- **📝 Outline**: Knowledge management and note-taking platform.
- **🖍 Excalidraw**: Collaborative whiteboard tool.
- **🛠 IT Tools**: Collection of IT utilities.
- **🔔 Changedetection.io**: Website change detection and monitoring.

### 📊 Monitoring
- **📈 Prometheus**: Metrics collection and alerting.
- **📊 Grafana**: Data visualization and analytics.
- **📡 Node Exporter**: System metrics exporter.
- **📶 MikroTik Exporter (MKTXP)**: Metrics for MikroTik devices.
- **📅 InfluxDB**: Time-series database for metrics storage.

### 🎥 Media
- **🎬 Plex**: Media server for streaming personal content.
- **🎞 Radarr**: Movie collection manager.
- **📺 Sonarr**: TV show collection manager.
- **📤 Transmission**: BitTorrent client.

### 💰 Money
- **💵 Repocket**: Passive income generation tool.
- **🐝 Honeygain**: Internet bandwidth sharing for rewards.
- **♟ Pawns**: Bandwidth sharing application.

### 📸 Immich
- **📷 Immich**: Self-hosted photo and video backup solution.
- **🗄 Postgres**: Database for Immich.
- **⚡ Redis**: Caching layer for Immich.

### 🏠 Homepage
- **🏡 Homepage**: A customizable dashboard for managing and monitoring the homelab.

## 🛠 Infrastructure

- **☸ Kubernetes**: The cluster is deployed on Kubernetes, leveraging its scalability and resilience.
- **📂 CephFS**: Used for persistent storage across applications.
- **🚦 Traefik**: Edge router and reverse proxy for managing ingress traffic.

## 📜 Deployment

The cluster is managed using GitOps principles with ArgoCD. Each application is defined in its respective YAML file under the `gitops` directory. Changes to the repository are automatically synchronized with the cluster.

### 🛠 Example Deployment

To deploy the `tools` namespace, ArgoCD uses the following configuration:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tools
spec:
  destination:
    namespace: tools
    server: https://kubernetes.default.svc
  source:
    path: tools
    repoURL: https://github.com/YogaNovvaindra/kube.git
    targetRevision: HEAD
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
## 🔒 Security

Sensitive data such as database credentials and API keys are managed using Sealed Secrets. These secrets are encrypted and stored securely in the repository.

## 🤝 Contributing
This repository is primarily for personal use, but feel free to explore and adapt it for your own homelab setup. Contributions and suggestions are welcome!

## 📜 License
This project is licensed under the MIT License.