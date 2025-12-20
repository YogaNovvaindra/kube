# Services

This directory contains various application services and their configurations.

## Featured Services

- **[Ghost](file:///home/yoga/Documents/kube/services/ghost.yml)**: Professional publishing platform.
- **[Portfolio](file:///home/yoga/Documents/kube/services/portfolio.yml)**: Personal project showcase.
- **[EcoGuardian](file:///home/yoga/Documents/kube/services/ecoguardian.yml)**: Environmental monitoring.
- **[Linear](file:///home/yoga/Documents/kube/services/linear-cred.yml)**: Issue tracking.
- **[Cloudflared](file:///home/yoga/Documents/kube/services/cloudflared.yml)**: Secure tunneling to the web.
- **[Project](file:///home/yoga/Documents/kube/services/project.yml)**: Personal projects.

## Shared Resources

- **`db-backup.yml`**: Generic database backup configuration for services.
- **`discord-cred.yml`**: Notification credentials for service alerts.
- **`mariadb-cred.yml`**: Database credentials.

## Cloudflare Tunnel Management

This service runs a `cloudflared` tunnel in **Local Management** mode. Configuration is defined in Kubernetes manifests, not the Cloudflare Dashboard.

### Adding a New Route

1.  **Update Config**: Edit `cloudflared-config.yml` to map the hostname to the Kubernetes service.
    ```yaml
    ingress:
      - hostname: "new-service.yoganova.my.id"
        service: http://service-name.namespace.svc.cluster.local:port
    ```
2.  **Add DNS Record**: Log in to the CLI and create the CNAME record.
    ```bash
    cloudflared tunnel route dns kube-tunnel new-service.yoganova.my.id
    ```
3.  **Deploy**: Apply the config change and restart the pods.
    ```bash
    kubectl apply -f cloudflared-config.yml
    kubectl rollout restart deployment cloudflared -n services
    ```

### Managing Credentials

If you need to rotate the tunnel token or update credentials:

1.  **Get New Token**:
    ```bash
    cloudflared tunnel token kube-tunnel
    ```
2.  **Seal & Update Secret**:

    ```bash
    kubectl create secret generic cloudflared-cred \
      --from-literal=TUNNEL_TOKEN='<NEW_TOKEN_STRING>' \
      --namespace services \
      --dry-run=client -o yaml | \
      kubeseal --cert ../sealed-secret/public-key.pem --format yaml > cloudflared-cred.yml

    kubectl apply -f cloudflared-cred.yml
    kubectl rollout restart deployment cloudflared -n services
    ```

### Troubleshooting

- **Check Status**: `kubectl get pods -n services -l app=cloudflared`
- **View Logs**: `kubectl logs -n services -l app=cloudflared --tail=20`
