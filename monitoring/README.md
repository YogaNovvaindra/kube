# Monitoring & Observability

The observability stack provides metrics, logging, and uptime monitoring for the entire cluster.

## Components

- **[Prometheus](monitoring/prometheus-deploy.yml)**: Metrics collection engine.
- **[Grafana](monitoring/grafana.yml)**: Dashboard visualization.
- **[Loki](monitoring/loki-deploy.yml)**: Log aggregation.
- **[Fluent-bit](monitoring/fluent-bit.yml)**: Log forwarding.
- **[Tempo](monitoring/tempo.yml)**: Distributed tracing backend.
- **[Uptime Kuma](monitoring/uptime/uptime-kuma.yml)**: External service monitoring.

## Exporters

Metrics are collected from various sources using dedicated exporters:

- Node Metrics (hardware)
- Kube State Metrics (cluster state)
- AdGuard, MikroTik, Proxmox, and SNMP exporters for hardware devices.
