# Prompt: Kickstart Development of a Live Video Stream Monitoring System

## 1. Project Goal & Overview

* **Primary Objective:** To create a centralized monitoring dashboard providing real-time health status for multiple live video streams originating from various sources. To compare health of the local network and hardware to confirm the end product is at the highest quality product possible.
* **Problem Solved:** Lack of unified visibility into stream health, leading to delayed issue detection during live events. Confirmation of end product compared to the possibilities the broadcast facility provides.
* **Target Users:** Broadcast engineers, Broadcast managers who want a single point of confirmation of a healthy broadcast output.
* **Success Criteria:** Ability to monitor a defined numnber streams concurrently, alerts trigger within 15 seconds of failure, provides clear visualization of key metrics.

## 2. Core Functionality & Requirements

* **Monitor Blackmagic Design Web Presenters:**
  * Models to Support: Web Presenter HD, Web Presenter 4K, flexibility to monitor future products, including from other manufacturers, i.e. Matrox Monarch.
  * Monitoring Method: JSON scraping of web interface, SNMP, future REST API's
  * Key Metrics: Streaming Status (On/Off), Input Status (Detected/Not Detected), Output Resolution, Output Bitrate, Internal Temperature, Error Messages.
* **Monitor Vimeo Live Streams:**
  * Monitoring Method: Vimeo API for live events, with enterprise access, youtube live
  * Authentication: API key
  * Key Metrics: Stream Status (Live/Offline), Current Viewer Count, Peak Viewer Count, Stream Health Score (if available), Input/Output Bitrate (if available), Latency (if available), future black and freeze detection
* **Monitor Generic Stream Health (via FFprobe/Similar):**
  * Tool Confirmation: FFProbe of GStream
  * Target Streams: Manually configured RTMP/SRT URLs, future coverage of higher end streams such as SMPTE 2110
  * Key Metrics: Resolution, Codec (Video/Audio), Bitrate (Actual Measured), Frame Rate, Packet Loss (if detectable), Timestamp Discontinuities (PTS/DTS errors), Buffer Health (if applicable).
* **Monitor Local Network Environment:**
  * Monitoring Scope: Network interface of the monitoring server, connectivity to Web Presenters, connectivity to Vimeo ingest points, general internet connectivity, Network Stability, Netowrk Latency, local internet bandwidth
  * Monitoring Methods: ICMP pings (latency, packet loss), interface bandwidth counters (SNMP on switches/routers, local OS commands like `ifconfig`/`ip`), potentially iperf tests? Need more useful options.
  * Key Metrics: Ping Latency (ms) to google and vimeo, Packet Loss (%) to gateway, Bandwidth Usage (Mbps/Gbps), Jitter (if measurable).
* **Alerting:**
  * Requirements: Alert if stream goes offline, if bitrate drops below threshold, if packet loss is excessive, if Web Presenter reports an error.Simple to understand one page interface. This needs to be seen on a single static 1080 display among a group of displays that are monitored by a broadcast engineers and managers. They need to know quickly if something needs to be investigated.
  * Notification Channels: Grafana alerts, email, simple GPIO activations on network devices, bitfocus companion

## 3. Proposed Technology Stack

* **Backend Logic:** Python Python 3.12.
  * Key Libraries to consider: `requests` , `subprocess` (for FFprobe), `python-vimeo` , `schedule` or `APScheduler`
* **Data Acquisition:** Custom Python scripts, JSON scraping
* **Time-Series Database:** Prometheus *or* InfluxDB. This is the hardest current decision
  * Rationale: Cannot decide if a push or pull model is better
* **Frontend / Visualization:** Grafana
  * Key Plugins: Standard Time series panels, Stat panels, Alerting features, potentially map panels if relevant
* **Operating System / Deployment:** Linux server (Ubuntu/Debian/CentOS), Docker container

## 4. High-Level Architecture Ideas (Optional)

* Monitoring of local envirnment
  * using tools like speedtest have a  lear view of system bandwidth and latency
* Data visualization
  * Data should be on a simple local display to cover approximately 30 minutes.
  * Historical data should be retrievable for 5 days by report, preferably printable.
* Stream Data
  * Include local hardware metrics
  * Include destination API metrics, where available
  * Include stream probing, understanding it will be swayed by local network
  * Provide easily understood comparisons to allow for recognizing trends
* Approachable configuration
  * Potential YAML file support
  * .env storage of sensitive data

## 5. Data Schema / Metrics Structure (Initial Thoughts)

* Well documented data structure
* Consistency for Grafana configuration and well structured use of tags

## 6. Non-Functional Requirements

* **Scalability:** currently needs to monitor 4 feeds and hardware, one network envirnment, as a FOSS project flexibility should be included
* **Performance:** Should be as quick aspossible, latency is bad. Polling frequency should be configurable to allow for hardware flexibility
* **Reliability:** High value data is at stake. Failure should be at least understood, i.e. failure of monitoring should be self displayed so if the information is unreliable it is understood as so.
* **Maintainability:** Would like the interface for configuration to be via a YAML doc. Interface should be limited to information conveyance.
* **Security:** Sensative information should be isolated, possibly in a .env file

## 7. Constraints & Considerations

* **Hardware:** Should be flexible and dependent on a docker deployment with needed background services.
* **Network:** a local managed network environment.

## 8. Desired Output / Next Steps (from LLM)

* **Request:**
  * "Provide a basic Python project structure (folders and key files) for this system."
  * Suggest an appropriate DB component with justification
  * Outline the configuration steps needed to have scrape metrics from multiple Python script endpoints.
  * Discuss the pros and cons of Prometheus vs. InfluxDB specifically for this video monitoring use case."
  * Provide a comprehensive task list and architecture document for this project

## 9. Memory Bank References

Comprehensive project documentation is maintained in the following Memory Bank files:

* **Project Context:**
  * `docs/productContext.md`: Product definitions and user needs
  * `docs/techContext.md`: Technical environment and dependencies
  * `docs/systemPatterns.md`: System design patterns and coding approaches

* **Project Status:**
  * `docs/tasks.md`: Current task list and priorities
  * `docs/status.md`: Project status overview and blockers
  * `docs/progress.md`: Implementation progress tracking
  * `docs/activeContext.md`: Current development focus

* **Architecture & Design:**
  * `docs/architecture.md`: System architecture and component design
  * `docs/technical.md`: Technical decisions and implementation details
