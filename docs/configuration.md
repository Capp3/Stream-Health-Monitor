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

The most important section that defines the streams to monitor:

```yaml
streams:
  - name: stream1
    provider:
      vimeolive:
        eventid: '1231231'
        vimeo_token: ${vimeo_token}
        vimeo_key: ${vimeo_key}
        vimeo_secret: ${vimeo_secret}
      polling_time: 2
    hardware:
      primary:
        webpresentor:
          ip_address: 192.168.1.100
      secondary:
        webpresentor:
          ip_address: 192.168.1.101
```

For each stream, you define:

#### Stream Name

A unique identifier for the stream.

#### Provider

The streaming provider configuration:

- Provider type (e.g., `vimeolive`, `rtmp`, `srt`)
- Provider-specific configuration (varies by provider type)
- **polling_time**: How often to poll this provider (in seconds)

#### Hardware

Hardware devices associated with this stream:

- **primary**: Primary hardware device configuration
  - Device type (e.g., `webpresentor`)
  - Device-specific configuration
- **secondary**: Optional backup hardware device configuration

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