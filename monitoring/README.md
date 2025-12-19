# Monitoring & Observability

The observability stack provides metrics, logging, and uptime monitoring for the entire cluster.

## Components

- **[Prometheus](file:///home/yoga/Documents/kube/monitoring/prometheus-deploy.yml)**: Metrics collection engine.
- **[Grafana](file:///home/yoga/Documents/kube/monitoring/grafana.yml)**: Dashboard visualization.
- **[Loki](file:///home/yoga/Documents/kube/monitoring/loki-deploy.yml)**: Log aggregation.
- **[Fluent-bit](file:///home/yoga/Documents/kube/monitoring/fluent-bit.yml)**: Log forwarding.
- **[Uptime Kuma](file:///home/yoga/Documents/kube/monitoring/uptime/uptime-kuma.yml)**: External service monitoring.

## Exporters

Metrics are collected from various sources using dedicated exporters:
- Node Metrics (hardware)
- Kube State Metrics (cluster state)
- AdGuard, MikroTik, Proxmox, and SNMP exporters for hardware devices.
