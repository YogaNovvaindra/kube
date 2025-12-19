# Keel

Keel provides automated container image updates by monitoring registries and updating deployments when new tags are available.

## Components

- **`keel.yml`**: Main deployment manifest.
- **`keel-cred.yml`**: Sealed secrets for registry authentication.
- **`notification.yml`**: Configuration for update notifications (e.g., Discord).

## Policies

Applications specify update policies via annotations:
- `keel.sh/policy: force`: Always update to the latest image.
- `keel.sh/trigger: poll`: Check for updates on a schedule.
- `keel.sh/match-tag: "true"`: Ensure tags match semver or specific patterns.
