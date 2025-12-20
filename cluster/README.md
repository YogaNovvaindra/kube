# Cluster Infrastructure

This directory contains core infrastructure utilities and cluster-wide management tools. These services are deployed in the `cluster` namespace to maintain clear separation from application workloads and core Kubernetes system components.

## 📦 Components

### [♻️ Cluster Reloader](reloader/reloader.yml)

Reloader automatically restarts Pods when their associated ConfigMaps or Secrets are updated. It monitors changes and performs rolling upgrades for Deployments, StatefulSets, and DaemonSets.

- **Primary Manifest**: `reloader/reloader.yml`

---

### [🔏 Cluster Sealed Secrets](sealed-secret/)

Sealed Secrets allow you to store encrypted secrets in Git safely. They can only be decrypted by the controller running in the cluster.

- **`sealed-secret/controller.yml`**: Deployment manifest for the Sealed Secrets controller.
- **`sealed-secret/backup.yml`**: CronJob for backing up the controller's active keys.

#### Usage: Sealing a Secret

To create a sealed secret file from a local template or literal:

```bash
kubeseal --format yaml < secret.yml > sealed-secret.yml
```

> [!IMPORTANT]
> The controller's active keys are backed up daily to `hostPath` storage via the backup CronJob.

---

### [🐋 Cluster Keel](keel/)

Keel provides automated container image updates by monitoring registries and updating deployments when new tags are available.

- **`keel/keel.yml`**: Main deployment manifest.
- **`keel/keel-cred.yml`**: Sealed secrets for registry authentication.
- **`keel/notification.yml`**: Configuration for update notifications (Discord bridge).

#### Policies

Applications specify update policies via annotations:

- `keel.sh/policy: force`: Always update to the latest image.
- `keel.sh/trigger: poll`: Check for updates on a schedule.
- `keel.sh/match-tag: "true"`: Ensure tags match semver or specific patterns.
