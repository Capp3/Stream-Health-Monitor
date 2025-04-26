# RTMP_HMonitor: Product Context

## Product Description

RTMP_HMonitor is a comprehensive live stream monitoring system designed for broadcast engineers and managers. It provides real-time health metrics for multiple video streams, enabling quick identification and resolution of issues during live broadcasts.

## Target Users

- **Broadcast Engineers:** Technical staff responsible for maintaining stream quality and resolving technical issues.
- **Broadcast Managers:** Supervisors who need a quick overview of broadcast health without technical details.

## Use Cases

1. **Real-time Stream Health Monitoring**
   - Users need to simultaneously monitor multiple live streams
   - System displays key health metrics for each stream
   - Visual indicators show status at a glance

2. **Stream Quality Verification**
   - Compare actual stream metrics with expected values
   - Verify streams meet quality standards
   - Document stream performance over time

3. **Issue Detection and Alert**
   - Quickly identify when streams go offline
   - Detect degradation in stream quality
   - Alert appropriate personnel to issues

4. **Network Environment Assessment**
   - Monitor local network conditions
   - Correlate network issues with stream performance
   - Identify infrastructure bottlenecks

## Key Requirements

- **Visibility:** Single-page dashboard viewable on a standard 1080p display
- **Responsiveness:** Alert within 15 seconds of stream failure
- **Clarity:** Simple, intuitive visual indicators for stream health
- **Reliability:** Accurate monitoring with self-diagnostics
- **Flexibility:** Support for various stream sources and protocols

## Success Metrics

- **Technical Success:**
  - Accurate detection of stream issues
  - Minimal false positives/negatives
  - Comprehensive metric collection
  - Reliable alerting system

- **User Success:**
  - Reduced time to detect stream issues
  - Improved understanding of stream health
  - Easier correlation of issues across streams
  - Better decision-making during technical problems

## Product Constraints

- **Display:** Must work effectively on a single 1080p monitor
- **Deployment:** Docker-based deployment for consistency
- **Configuration:** YAML-based configuration for clarity
- **Security:** Environment variable storage for sensitive data

## Integration Points

- **Stream Sources:**
  - RTMP/SRT streams via FFprobe
  - Blackmagic Web Presenters via JSON scraping
  - Vimeo live streams via API
  - Future expansion to additional sources

- **Visualization:**
  - Grafana for dashboards and visualizations
  - Alert notifications via multiple channels

- **Infrastructure:**
  - Network monitoring integration
  - Hardware metrics collection
