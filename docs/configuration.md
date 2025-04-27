# RTMP_HMonitor Configuration Guide

RTMP_HMonitor uses a YAML-based configuration system that allows for flexible setup of monitoring for multiple streams, hardware devices, and streaming providers.

## Configuration File Location

By default, the application looks for the configuration file at:

```
config/config.yml
```

You can override this location by setting the `CONFIG_PATH` environment variable.

## Configuration Structure

The configuration file has the following main sections:

1. **backend**: Core system configuration
2. **speedtest**: Optional network speed testing settings
3. **streams**: Stream-specific monitoring configuration

### Backend Configuration

The backend section configures the core system components:

```yaml
backend:
  database:
    - type: prometheus
      host: localhost
      port: 9090
      username: rtmphm
      password: rtmphm
  reporting:
    - type: json_output
      port: 12000
  logging:
    level: debug
    location: logs/rtmphm.log
    retention: 10
  networking:
    interface: eth0
```

#### Database

Supports multiple database configurations:

- **type**: Database type (`prometheus` or `influxdb`)
- **host**: Database hostname or IP address
- **port**: Database port
- **username**: Optional database username
- **password**: Optional database password

#### Reporting

Configures output methods for monitoring data:

- **type**: Reporting type (`json_output`, `websocket`, or `http_api`)
- **port**: Port to serve the reporting data

#### Logging

Configure application logging:

- **level**: Log level (`debug`, `info`, `warning`, or `error`)
- **location**: Log file path
- **retention**: Log retention period in days

#### Networking

Configure network settings:

- **interface**: Network interface to use for monitoring

### Speedtest Configuration

Optional configuration for network speed testing:

```yaml
speedtest:
  polling_time: 10
  server: optional_server_url
```

- **polling_time**: How often to run speed tests (in seconds)
- **server**: Optional specific speedtest server to use

### Streams Configuration

The most important section defines the streams to monitor. Each stream can have multiple providers (API-based or direct HLS) and multiple hardware encoders tagged as primary/secondary, allowing flexible health checks across different sources.

```yaml
streams:
  - name: "Local RTMP Stream"
    enabled: true
    polling_interval: 30
    providers:
      - type: ffprobe
        label: "RTMP Source"
        url: "rtmp://example.com/live/stream1"

  - name: "Studio Encoder"
    enabled: true
    polling_interval: 15
    providers:
      - type: web_presenter
        label: "Primary Encoder"
        host: "192.168.1.100"
        api_path: "/status.json"
      - type: web_presenter
        label: "Secondary Encoder"
        host: "192.168.1.101"
        api_path: "/status.json"

  - name: "Vimeo Live Event"
    enabled: true
    polling_interval: 60
    providers:
      - type: vimeo
        label: "Vimeo API"
        event_id: "123456"
        api_key_env: "VIMEO_API_KEY"  # Vimeo API token to fetch HLS link
      - type: ffprobe
        label: "Vimeo HLS"
        url: "https://player.vimeo.com/event/123456/hls.m3u8"

  - name: "YouTube Live Stream"
    enabled: true
    polling_interval: 60
    providers:
      - type: youtube
        label: "YouTube API"
        video_id: "abcd1234"
        api_key_env: "YOUTUBE_API_KEY"
      - type: http
        label: "YouTube HLS"
        url: "https://youtube.com/hls/abcd1234.m3u8"
```

Key Points:
- Multiple providers per stream: allows API-driven health checks and direct HLS probing.
- Vimeo: use API to retrieve m3u8 link, then probe via ffprobe/GStreamer.
- Hardware encoders: tag primary/secondary devices for Web Presenters.
- Dynamic streams (e.g., YouTube Live) can be monitored without dedicated hardware.

## Environment Variables

The configuration supports environment variable substitution with default values:

```yaml
host: ${DB_HOST:-localhost}
```

This syntax will use the value of the `DB_HOST` environment variable, or `localhost` if not set.

## Extending the Configuration

### Adding New Provider Types

The system is designed to be extensible. To add a new provider type:

1. Create a new provider implementation
2. Add the provider-specific configuration to a stream:

```yaml
streams:
  - name: new_stream
    provider:
      new_provider_type:
        option1: value1
        option2: value2
```

### Adding New Hardware Types

Similarly, to add support for a new hardware device:

1. Create a new hardware device implementation
2. Add the hardware-specific configuration:

```yaml
hardware:
  primary:
    new_hardware_type:
      setting1: value1
      setting2: value2
```

## Configuration Validation

The configuration is validated on application startup. If there are any errors, they will be reported in the logs. Common validation checks include:

- Required fields
- Enumeration validation (e.g., log levels)
- Type checking
- Provider-specific validation
- Hardware-specific validation

## Examples

### Basic Configuration

```yaml
backend:
  database:
    - type: prometheus
      host: localhost
      port: 9090
  reporting:
    - type: json_output
      port: 12000
  logging:
    level: info
    location: logs/rtmphm.log
    retention: 7
  networking:
    interface: eth0
streams:
  - name: main_stream
    provider:
      rtmp:
        url: rtmp://streaming.example.com/live/stream
      polling_time: 5
    hardware:
      primary:
        webpresentor:
          ip_address: 192.168.1.100
```

### Multi-Stream Configuration

See the full `config.yml` example for a multi-stream configuration. 