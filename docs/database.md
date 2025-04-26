# RTMP_HMonitor Database Configuration

This document outlines the database configuration for the RTMP_HMonitor project, which uses Prometheus as its primary time-series database.

## Database Selection

After evaluating different time-series databases, Prometheus was selected for the following reasons:

1. **Monitoring-focused**: Prometheus is specifically designed for monitoring and alerting, making it an ideal choice for this application.
2. **Pull-based architecture**: The pull-based model fits well with our metrics collection approach.
3. **Simple deployment**: Easy to set up and maintain with minimal configuration.
4. **Query language**: PromQL provides powerful querying capabilities for time-series data.
5. **Integration**: Excellent integration with Grafana for visualization.

## Prometheus Configuration

The Prometheus configuration is stored in the `prometheus/` directory and consists of:

### prometheus.yml

This is the main Prometheus configuration file that defines:

- Global settings (scrape and evaluation intervals)
- Scrape configurations (endpoints to collect metrics from)
- Alerting rules configuration
- AlertManager integration

```yaml
global:
  scrape_interval: 1s
  evaluation_interval: 5s

# Scrape configurations
scrape_configs:
  # RTMP_HMonitor API
  - job_name: 'rtmp_hmonitor'
    static_configs:
      - targets: ['api:5000']  # Using Docker service name
    metrics_path: '/metrics'

# Alerting rules
rule_files:
  - 'alerts.yml'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']  # Using Docker service name
```

### alerts.yml

This file contains the alerting rules for Prometheus, including:

- Stream health alerts (bitrate, FPS)
- Network-related alerts (latency, packet loss)
- System performance alerts

## Data Storage

Prometheus stores its time-series data on disk in a custom format optimized for time-series data. In our Docker setup, this data is persisted using a named volume (`prometheus_data`).

## Metrics Collection

The RTMP_HMonitor FastAPI application exposes metrics at the `/metrics` endpoint in the Prometheus format. These metrics include:

- `rtmp_stream_bitrate`: Current bitrate of RTMP streams
- `rtmp_stream_fps`: Frames per second of RTMP streams
- `rtmp_stream_errors`: Count of detected errors in streams
- `network_latency`: Network latency to monitored endpoints
- `network_packet_loss`: Percentage of packet loss to endpoints
- `ffprobe_processing_time`: Time spent processing FFprobe results

## Visualization

Grafana is used to visualize the metrics stored in Prometheus. The Grafana configuration includes:

- Prometheus datasource configuration
- Dashboards for different aspects of monitoring
- Alert visualization panels

## Deployment

The entire monitoring stack is deployed using Docker Compose, with containers for:

- The RTMP_HMonitor API
- Prometheus
- AlertManager
- Grafana

## Maintenance

### Data Retention

By default, Prometheus retains data for 15 days. This can be configured using the `--storage.tsdb.retention.time` parameter in the Prometheus container configuration.

### Backup

To backup Prometheus data, you can either:

1. Copy the data directly from the Docker volume
2. Use Prometheus's snapshot API to create a consistent backup

## Troubleshooting

Common issues and their solutions:

1. **Missing metrics**: Ensure the API is running and accessible to Prometheus
2. **Query errors**: Check PromQL syntax and ensure metrics exist
3. **High disk usage**: Adjust retention period or consider using remote storage

## Future Enhancements

Planned improvements to the database setup:

1. Implementing longer-term storage using remote write
2. Adding redundancy for high availability
3. Optimizing query performance for complex dashboards
4. Implementing metric compaction for historical data 