# RTMP_HMonitor Technical Documentation

## Development Environment

* **Python Version:** 3.12
* **Package Manager:** UV (Rust-based Python package manager)
* **Virtual Environment:** venv
* **Environment Activation:** All commands must be executed within the activated virtual environment (e.g., `source venv/bin/activate`).
* **IDE Recommendations:** VS Code with Python extensions

## Dependencies and Libraries

* **Core Dependencies:**
  * `requests`: For HTTP requests and API interactions
  * `pyyaml`: For YAML configuration parsing
  * `schedule`: For scheduling regular monitoring tasks
  * `python-dotenv`: For environment variable management

* **Stream Monitoring:**
  * `subprocess`: For invoking FFprobe
  * `python-vimeo`: For Vimeo API integration

* **Network Monitoring:**
  * `ping3`: For ICMP ping operations
  * `psutil`: For local system metrics

* **Database Clients:**
  * `prometheus-client`: For Prometheus integration
  * `influxdb-client`: For InfluxDB integration

## Package Management with UV

* **Why UV:**
  * Significantly faster installation times compared to pip
  * Reliable dependency resolution
  * Built-in caching for faster reinstalls
  * Improved virtual environment management

* **Best Practices:**
  * **Install all dependencies using UV** so they are automatically tracked in `pyproject.toml`:
    ```bash
    uv pip install <package_name> --update
    ```
  * To install from requirements:
    ```bash
    uv pip install -r requirements.txt
    ```
  * **Always update `pyproject.toml`** via UV when adding new packages.
  * **Ensure UV commands are run inside the venv** to keep project dependencies isolated.

* **Installation:**
  * Direct installation: `curl -sSf https://install.python-uv.org | python3`
  * Via pip: `pip install uv`

* **Basic Usage:**
  * Create virtual environment: `uv venv venv`
  * Install dependencies: `uv pip install -r requirements.txt`
  * Add package: `uv pip install package_name --update`

* **Performance Benefits:**
  * Local development: Faster setup and iteration
  * CI/CD pipelines: Reduced build times
  * Containerization: Faster image building

## Code Structure

* **Main Application Components:**
  * `rtmpmonitor.py`: Main entry point
  * `src/main.py`: Core application logic
  * `src/threads.py`: Thread management
  * `src/attributes/`: Data models and attributes

* **Monitoring Modules:**
  * `src/monitors/`: Collection of monitoring implementations
  * `src/exporters/`: Database exporters

* **Configuration:**
  * `config/`: Configuration files
  * `config/.env.sample`: Template for environment variables

## Technical Decisions

### Database Selection Considerations

**Prometheus:**

* Advantages:
  * Pull-based model fits monitoring servers well
  * Built-in service discovery
  * Native support in Grafana
  * Simpler to deploy and scale
* Disadvantages:
  * Less efficient with high-cardinality data
  * More complex query language

**InfluxDB:**

* Advantages:
  * Push-based model can be easier for some use cases
  * Better handling of high-cardinality data
  * Flux query language is more powerful
  * Better for long-term storage
* Disadvantages:
  * More complex setup
  * Additional client libraries needed

### FFprobe vs GStreamer

* FFprobe selected for initial implementation due to:
  * More widely used in video monitoring
  * Simpler command-line interface
  * Better documentation
  * More consistent output format

* GStreamer consideration for future expansion:
  * Better for real-time analysis
  * More flexible pipeline capabilities
  * More resource-intensive

### Threading Model

* Separate threads for each monitor type to prevent blocking
* Centralized thread management in `threads.py`
* Thread-safe data structures for metric collection

## Implementation Notes

### Stream Health Monitoring

* FFprobe commands standardized to extract consistent metrics
* Retry mechanism for transient stream issues
* Cached results to prevent unnecessary processing

### Web Presenter Monitoring

* JSON parsing with fallback mechanisms
* Error handling for connection issues
* Rate limiting to prevent overloading devices

### Network Monitoring

* Configurable ping targets
* Rolling average calculations
* Bandwidth monitoring leverages psutil

## Configuration System

* YAML-based configuration for readability
* Environment variables for sensitive information
* Runtime configuration updates where possible

## Planned Improvements

* Implement full plugin architecture
* Add advanced alert correlation
* Improve historical data analysis
* Add machine learning for anomaly detection
