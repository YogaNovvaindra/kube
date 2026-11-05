# 🛠️ Tools & Utilities

A collection of utility tools, development environments, automation platforms, and storage solutions.

## 📂 Structure

### 🤖 AI & LLM (`ai/`)
- **[FreeLLMAPI](ai/freellmapi.yml)**: OpenAI-compatible API and dashboard aggregating free LLM providers

### 🤖 Automation (`automation/`)
- **[n8n](automation/n8n.yml)**: Workflow automation platform
- **[Home Assistant](automation/homeassistant.yml)**: Open source home automation that puts local control and privacy first
- **[ESPHome](automation/esphome.yml)**: System that lets you control your ESP boards
- **[Authensa](automation/authensa.yml)**: Autonomous Product Engine & AI Agent Orchestration (Mission Control)
- **[OpenClaw](automation/openclaw.yml)**: AI Agent Gateway Runtime for Authensa
- **[Hermes and Firecrawl Compose stack](../docker-compose/hermes-firecrawl/README.md)**: Docker Compose setup for running both services and Firecrawl dependencies outside Kubernetes

### 🔐 Security & Identity (`authentik/`, `security/`)
- **[Authentik](authentik/authentik.yml)**: Identity and Access Management (SSO) acting as the central identity provider
- **[Vaultwarden](security/vaultwarden.yml)**: Self-hosted Bitwarden-compatible password manager

### 🗄️ Storage & File Management (`storage/`)
- **[RustFS](storage/rustfs.yml)**: S3-compatible object storage solution
- **[FileBrowser](storage/filebrowser.yml)**: Web-based file manager
- **[Samba](storage/samba.yml)**: SMB/CIFS file sharing server mapped to CephFS

### 💻 Editors & Document Tools (`editor/`)
- **[Outline](editor/outline.yml)**: Collaborative knowledge base and wiki
- **[Excalidraw](editor/excalidraw.yml)**: Virtual collaborative whiteboard
- **[BentoPDF](editor/bentopdf.yml)**: Self-hosted PDF manipulation tools
- **[Vert](editor/vert.yml)**: Clean and simple RSS feed reader

### 🌐 Cluster & Networking (`cluster/`, `network/`)
- **[Semaphore](cluster/semaphore.yml)**: UI for running Ansible playbooks
- **[Netbird](cluster/netbird.yml)**: Mesh VPN and P2P networking
- **[Syncthing](cluster/syncthing.yml)**: Continuous file synchronization
- **[Speedtest](network/speedtest.yml)**: Internet connection speed testing

### 🛠️ Developer Utilities (`utilities/`, `git/`)
- **[IT-Tools](utilities/it-tools.yml)**: Collection of handy online tools for developers
- **[Gitea](git/gitea.yml)**: Self-hosted Git service with scheduled GitHub repository mirrors, including kubeseal-ui

### 📦 Archiving (`archiving/`)
- **[Warrior](archiving/warrior.yml)**: Archive Team Warrior for distributed archiving

### 🏠 Dashboard (`homepage/`)
- **[Homepage](homepage/homepage.yml)**: Central dashboard for accessing all homelab services

## FreeLLMAPI setup

FreeLLMAPI requires a persistent `ENCRYPTION_KEY` in production. Create and seal
the key before syncing the application; do not commit an unsealed Kubernetes
Secret:

```bash
kubectl create secret generic freellmapi-cred \
  --namespace tools \
  --from-literal=ENCRYPTION_KEY="$(openssl rand -hex 32)" \
  --dry-run=client -o yaml |
  kubeseal --format yaml > ai/freellmapi-cred.yml
```

Keep the same key with the persistent application data when backing up or
restoring FreeLLMAPI, since provider keys stored by the app are encrypted with
it.
