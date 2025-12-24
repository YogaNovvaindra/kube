# Immich

Immich is a self-hosted high-performance backup solution for photos and videos, with a focus on mobile device sync.

## Components

- **[`immich.yml`](file:///home/yoga/Documents/kube/immich/immich.yml)**: The core Immich application, migrated to the official microservices architecture:
  - **`immich-server`**: Main application logic (v2.4.1).
  - **`immich-machine-learning`**: Machine learning worker (v2.4.1-openvino) with Intel Graphics acceleration (`/dev/dri`).
- **[`db-cred.yml`](file:///home/yoga/Documents/kube/immich/db-cred.yml)**: Sealed credentials for the PostgreSQL database.
- **[`db-backup.yml`](file:///home/yoga/Documents/kube/immich/db-backup.yml)**: Automated database backup jobs.
- **[`discord-cred.yml`](file:///home/yoga/Documents/kube/immich/discord-cred.yml)**: Discord integration for update notifications.

## Usage

Immich works best with its mobile application (Android/iOS) to automatically back up your photos to this cluster. The current deployment leverages Intel QuickSync for transcoding and OpenVINO for machine learning acceleration.
