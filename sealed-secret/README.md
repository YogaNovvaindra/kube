# Sealed Secrets

Sealed Secrets allow you to store encrypted secrets in Git safely. They can only be decrypted by the controller running in the cluster.

## Usage

### Sealing a Secret
To create a sealed secret file from a local template or literal:
```bash
kubeseal --cert sealed-secret/public-key.pem -f homepage/homepage-cred-.tml -o yaml > homepage/homepage-cred.yml
```

### Infrastructure Components
- **`public-key.pem`**: The public key used by `kubeseal` to encrypt secrets.
- **`sealed-secret.yml`**: Deployment manifest for the Sealed Secrets controller.

> [!IMPORTANT]
> Always use the `--cert` flag with the local public key to ensure consistency across different environments.