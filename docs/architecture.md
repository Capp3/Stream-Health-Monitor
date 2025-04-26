# RTMP_HMonitor Architecture

## System Overview

The RTMP_HMonitor system is designed to provide real-time monitoring of RTMP streams, network connectivity, and associated services. The architecture follows a modular design with clean separation of concerns for scalability and maintainability.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           RTMP_HMonitor                             │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────┤
│  Data       │  Collection │  Storage    │  Analysis   │  Visualization│
│  Sources    │  Layer      │  Layer      │  Layer      │  Layer      │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │
│ │ RTMP    │ │ │ FFprobe │ │ │         │ │ │         │ │ │         │ │
│ │ Streams │─┼─┤ Workers │─┼─┤         │ │ │         │ │ │         │ │
│ └─────────┘ │ └─────────┘ │ │         │ │ │         │ │ │         │ │
│ ┌─────────┐ │ ┌─────────┐ │ │         │ │ │         │ │ │         │ │
│ │ Network │ │ │ Network │ │ │         │ │ │         │ │ │         │ │
│ │ Services│─┼─┤ Monitor │─┼─┤         │ │ │ Prometheus│ │ Grafana  │ │
│ └─────────┘ │ └─────────┘ │ │ Metrics │─┼─┤ Alert    │─┼─┤ Dashboards│
│ ┌─────────┐ │ ┌─────────┐ │ │ Database│ │ │ Manager  │ │ │         │ │
│ │ Web     │ │ │ API     │ │ │         │ │ │         │ │ │         │ │
│ │ Presenter│─┼─┤ Scraper │─┼─┤         │ │ │         │ │ │         │ │
│ └─────────┘ │ └─────────┘ │ │         │ │ │         │ │ │         │ │
│ ┌─────────┐ │ ┌─────────┐ │ │         │ │ │         │ │ │         │ │
│ │ Vimeo   │ │ │ Vimeo   │ │ │         │ │ │         │ │ │         │ │
│ │ API     │─┼─┤ Client  │─┼─┤         │ │ │         │ │ │         │ │
│ └─────────┘ │ └─────────┘ │ └─────────┘ │ └─────────┘ │ └─────────┘ │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

## Core Components

### 1. Collection Layer

#### 1.1 HTTP API Service
- **Purpose**: Central component that exposes metrics and coordinates data collection
- **Technology**: FastAPI
- **Responsibilities**:
  - Exposing Prometheus metrics endpoint
  - Coordinating worker threads
  - Providing health checks and status APIs
  - Managing configuration

#### 1.2 FFprobe Workers
- **Purpose**: Analyze RTMP streams to extract quality metrics
- **Technology**: Python with concurrent.futures
- **Responsibilities**:
  - Running FFprobe in separate threads to avoid blocking
  - Caching results to handle Prometheus scrape requests
  - Extracting key metrics (bitrate, FPS, codec info)
  - Detecting stream errors and outages

#### 1.3 Network Monitor
- **Purpose**: Monitor network connectivity and performance
- **Technology**: Python with ping/socket libraries
- **Responsibilities**:
  - Measuring latency to key endpoints
  - Detecting packet loss
  - Monitoring bandwidth availability
  - Checking service connectivity

#### 1.4 Web Presenter Client
- **Purpose**: Extract metrics from Blackmagic Web Presenter
- **Technology**: Python with requests
- **Responsibilities**:
  - Scraping JSON data from Web Presenter API
  - Standardizing metrics for storage
  - Detecting device status changes

#### 1.5 Vimeo API Client
- **Purpose**: Retrieve stream information from Vimeo
- **Technology**: Python with Vimeo SDK
- **Responsibilities**:
  - Authenticating with Vimeo API
  - Retrieving stream status and viewer counts
  - Detecting stream health indicators from Vimeo

### 2. Storage Layer

#### 2.1 Prometheus
- **Purpose**: Time-series database for metrics storage
- **Responsibilities**:
  - Scraping metrics from HTTP endpoints
  - Storing time-series data
  - Providing query capabilities
  - Supporting alerting rules

### 3. Analysis Layer

#### 3.1 Prometheus Alert Manager
- **Purpose**: Process and route alerts
- **Responsibilities**:
  - Evaluating alert rules
  - Grouping and aggregating alerts
  - Routing notifications to appropriate channels
  - Managing alert status (firing, resolved)

### 4. Visualization Layer

#### 4.1 Grafana
- **Purpose**: Visualize metrics and alerts
- **Responsibilities**:
  - Displaying real-time dashboards
  - Visualizing historical trends
  - Supporting alerts visualization
  - Providing user-friendly interface for metrics exploration

## Component Interfaces

### 1. HTTP API Service Interfaces

#### 1.1 External Interfaces
- **Metrics Endpoint** (`/metrics`): Prometheus-formatted metrics
- **Health Endpoint** (`/health`): Service health information
- **Status API** (`/api/v1/status`): Overall system status

#### 1.2 Internal Interfaces
- **FFprobe Worker Interface**: Asynchronous job submission and result retrieval
- **Configuration Interface**: Environment-based configuration loading
- **Metrics Registry**: Interface for registering and updating Prometheus metrics

### 2. Storage Interfaces

#### 2.1 Prometheus Interfaces
- **Scrape Interface**: HTTP-based metric collection from targets
- **Query Interface**: PromQL for data retrieval
- **Alert Rules Interface**: YAML-based alert definition

### 3. Visualization Interfaces

#### 3.1 Grafana Interfaces
- **Data Source Interface**: Connection to Prometheus
- **Dashboard Interface**: JSON-based dashboard definition
- **Alert Interface**: Connection to Prometheus Alertmanager

## Data Flows

### 1. Metrics Collection Flow
1. FFprobe Workers analyze RTMP streams in background threads
2. Workers update in-memory metrics registry with results
3. Prometheus scrapes `/metrics` endpoint at 1-second intervals
4. Time-series data is stored in Prometheus database

### 2. Alerting Flow
1. Prometheus evaluates alert rules against time-series data
2. When thresholds are crossed, alerts are sent to Alertmanager
3. Alertmanager groups, deduplicates, and routes alerts
4. Notifications are sent to configured receivers (email, Slack)

### 3. Visualization Flow
1. Grafana queries Prometheus for dashboard data
2. Dashboards display real-time and historical metrics
3. Users interact with dashboards to explore data
4. Alert status is visualized in dashboards

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose Stack                         │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │ ┌───────────┐ │
│  │           │  │  │           │  │  │           │  │ │           │ │
│  │ RTMP      │  │  │ Prometheus│  │  │AlertManager│  │ │ Grafana   │ │
│  │ Monitor   │  │  │           │  │  │           │  │ │           │ │
│  │ API       │  │  │           │  │  │           │  │ │           │ │
│  │           │  │  │           │  │  │           │  │ │           │ │
│  └───────────┘  │  └───────────┘  │  └───────────┘  │ └───────────┘ │
│       │         │        │        │        │        │       │       │
├───────┼─────────┼────────┼────────┼────────┼────────┼───────┼───────┤
│       │         │        │        │        │        │       │       │
│       │         │        │        │        │        │       │       │
│       ▼         │        ▼        │        ▼        │       ▼       │
│  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │ ┌───────────┐ │
│  │ logs      │  │  │ prometheus│  │  │alertmanager│  │ │ grafana   │ │
│  │ volume    │  │  │ volume    │  │  │ volume    │  │ │ volume    │ │
│  └───────────┘  │  └───────────┘  │  └───────────┘  │ └───────────┘ │
└─────────────────┴─────────────────┴─────────────────┴───────────────┘
```

## Future ELK Stack Integration

The architecture is designed to be extensible for future integration with an Elasticsearch, Logstash, and Kibana (ELK) stack to provide enhanced logging, searching, and visualization capabilities.

### ELK Stack Benefits for RTMP_HMonitor

1. **Enhanced Log Management**:
   - Centralized storage of application logs
   - Structured logging with rich querying capabilities
   - Log correlation across components

2. **Advanced Search and Analysis**:
   - Full-text search across logs and events
   - Complex querying for incident investigation
   - Anomaly detection for stream behavior

3. **Extended Visualization**:
   - Unified dashboards combining metrics and logs
   - Custom visualizations for stream quality analysis
   - Timeline views for event correlation

### Planned ELK Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Enhanced Architecture                        │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────┤
│ RTMP_HMonitor│   Prometheus │  ELK Stack   │   Grafana    │Alerting │
│   Components │     Stack    │              │              │  Stack  │
├──────────────┼──────────────┼──────────────┼──────────────┼─────────┤
│              │              │              │              │         │
│ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │┌───────┐│
│ │API Service│ │ │Prometheus│ │ │Elastic-  │ │ │Grafana   │ ││Alert- ││
│ │+ Workers  │─┼─┤          │ │ │search    │ │ │Dashboards│ ││Manager││
│ └──────────┘ │ └──────────┘ │ └──────────┘ │ └──────────┘ │└───────┘│
│      │       │      │       │      ▲       │      │       │    │    │
│      │       │      │       │      │       │      │       │    │    │
│      │       │      │       │      │       │      │       │    │    │
│      │       │      ▼       │      │       │      │       │    │    │
│      │       │ ┌──────────┐ │ ┌──────────┐ │      │       │    │    │
│      └───────┼─┤Metric Data│ │ │Log Data  │◄┼──────┼───────┼────┘    │
│      │       │ └──────────┘ │ └──────────┘ │      │       │         │
│      │       │              │      ▲       │      │       │         │
│      │       │              │      │       │      │       │         │
│      ▼       │              │      │       │      ▼       │         │
│ ┌──────────┐ │              │ ┌──────────┐ │ ┌──────────┐ │         │
│ │Structured│ │              │ │Logstash  │ │ │Kibana    │ │         │
│ │Logs      │─┼──────────────┼─┤          │ │ │Dashboards│ │         │
│ └──────────┘ │              │ └──────────┘ │ └──────────┘ │         │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘
```

### ELK Stack Implementation Steps

1. **Phase 1: Structured Logging**
   - Implement structured logging in all components
   - Define consistent log format with metadata
   - Create log rotation and archival strategy

2. **Phase 2: ELK Core Setup**
   - Deploy Elasticsearch for log storage
   - Configure Logstash for log ingestion and transformation
   - Set up Kibana for log visualization

3. **Phase 3: Integration**
   - Implement log forwarding from applications to Logstash
   - Create index patterns in Elasticsearch
   - Develop Kibana dashboards for log analysis

4. **Phase 4: Advanced Features**
   - Implement log-based alerting
   - Configure anomaly detection
   - Create unified dashboards with Grafana and Kibana

### Benefits of Dual Monitoring Approach

The combination of Prometheus for metrics and ELK for logs provides a comprehensive monitoring solution:

1. **Metrics-based Monitoring (Prometheus)**:
   - Real-time numerical metrics at second/sub-second resolution
   - Efficient time-series storage optimized for metrics
   - Threshold-based alerting on quantitative measures

2. **Log-based Monitoring (ELK)**:
   - Rich contextual information for troubleshooting
   - Qualitative event data with full-text search
   - Historical analysis with flexible retention policies

3. **Unified Visibility**:
   - Correlated view of metrics and logs
   - Multiple visualization options
   - Comprehensive alerting capabilities

## Architecture Evolution Plan

1. **Current Implementation (Phase 1)**:
   - Prometheus-based metrics collection and storage
   - FFprobe worker multithreading for RTMP analysis
   - Basic alerting and visualization with Grafana

2. **Short-term Enhancements**:
   - Complete network monitoring implementation
   - Implement Web Presenter integration
   - Develop comprehensive Grafana dashboards

3. **Medium-term Expansion**:
   - Add Vimeo API integration
   - Enhance alerting capabilities
   - Implement more sophisticated stream health assessment

4. **Long-term Evolution**:
   - Integrate ELK stack for log management
   - Implement advanced analytics capabilities
   - Develop unified monitoring and troubleshooting interface

## Component Scalability Considerations

### 1. Collection Layer Scalability
- FFprobe workers can be scaled horizontally with more threads
- API service can be deployed in multiple instances behind load balancer
- Collection components can be distributed across multiple servers

### 2. Storage Layer Scalability
- Prometheus federation for larger deployments
- Configurable retention and aggregation policies
- Potential sharding of metrics across multiple instances

### 3. ELK Stack Scalability
- Elasticsearch cluster for distributed log storage
- Multiple Logstash instances for high throughput
- Configurable index lifecycle management

## Conclusion

The RTMP_HMonitor architecture provides a flexible, modular approach to real-time stream monitoring. The current implementation focuses on metrics collection using Prometheus, with a planned evolution path to incorporate ELK stack for enhanced logging and analysis capabilities.

The system is designed to scale from single-instance deployments to distributed architectures based on monitoring needs, with clear separation of concerns between collection, storage, analysis, and visualization layers.
