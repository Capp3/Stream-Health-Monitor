# Stream Health Monitor - Project Structure

## Directory Structure

```
stream-health-monitor/
├── config/                   # Configuration files
│   ├── .env.sample           # Sample environment variables template
│   └── config.yaml.sample    # Sample YAML configuration
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture and design
│   ├── database_decision.md  # Database selection analysis
│   ├── implementation_plan.md # Implementation strategy
│   ├── project_structure.md  # This document
│   └── technical.md          # Technical decisions
├── logs/                     # Log files directory
├── src/                      # Source code
│   └── stream_health_monitor/ # Main package
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Entry point for direct execution
│       ├── api/              # API service module
│       │   ├── __init__.py
│       │   ├── app.py        # FastAPI application
│       │   └── routes/       # API endpoints
│       ├── config/           # Configuration module
│       │   ├── __init__.py
│       │   └── loader.py     # Configuration loading utilities
│       ├── db/               # Database module
│       │   ├── __init__.py
│       │   └── metrics.py    # Metrics schema and storage
│       ├── monitors/         # Monitoring modules
│       │   ├── __init__.py
│       │   ├── ffprobe.py    # FFprobe monitoring
│       │   ├── network.py    # Network monitoring
│       │   ├── vimeo.py      # Vimeo API monitoring
│       │   └── webpresenter.py # Web Presenter monitoring
│       └── utils/            # Utility functions
│           ├── __init__.py
│           └── logging.py    # Logging configuration
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── .env                      # Environment variables (not in version control)
├── .gitignore                # Git ignore file
├── CONTRIBUTING.md           # Contribution guidelines
├── docker-compose.yaml       # Docker Compose configuration
├── Dockerfile                # Docker build configuration
├── LICENSE                   # Project license
├── Makefile                  # Development automation
├── pyproject.toml            # Python package configuration
├── README.md                 # Project overview
└── tox.ini                   # Tox configuration for testing
```

## Key Components

### Source Code Structure

#### Main Package (`stream_health_monitor`)

The core package containing all the application code.

#### API Module (`api/`)

FastAPI application providing HTTP endpoints for metrics and management.

* `app.py`: FastAPI application setup
* `routes/`: API endpoints for different services

#### Configuration Module (`config/`)

Handles loading and validation of configuration from YAML and environment.

* `loader.py`: Utilities for loading and validating configuration

#### Database Module (`db/`)

Manages interaction with the time-series database (Prometheus).

* `metrics.py`: Defines metrics schema and storage interfaces

#### Monitoring Modules (`monitors/`)

Contains modules for each type of monitoring target.

* `ffprobe.py`: Monitors generic streams using FFprobe
* `network.py`: Monitors network conditions and connectivity
* `vimeo.py`: Monitors Vimeo streams via the API
* `webpresenter.py`: Monitors Blackmagic Web Presenters

#### Utilities (`utils/`)

Common utility functions used across the application.

* `logging.py`: Configures application logging

### Configuration Files

#### Environment Variables (`.env`)

Contains sensitive configuration like:
* API keys
* Authentication credentials
* Service endpoints

#### YAML Configuration (`config/config.yaml`)

Contains non-sensitive configuration like:
* Stream URLs and metadata
* Monitoring intervals
* Alert thresholds
* General system settings

### Docker Configuration

#### Dockerfile

Defines the container build for the Stream Health Monitor application.

#### Docker Compose (`docker-compose.yaml`)

Orchestrates:
* Stream Health Monitor application
* Prometheus for metrics storage
* AlertManager for alerting
* Grafana for visualization

## Development Workflow

The project follows a standard Python development workflow:

1. Use `pyproject.toml` for package configuration
2. Manage dependencies with `pip` or a tool like `poetry`
3. Use `tox` for running tests across environments
4. Utilize `Makefile` for common development tasks

## Testing Structure

### Unit Tests (`tests/unit/`)

Tests for individual components in isolation.

### Integration Tests (`tests/integration/`)

Tests interactions between components and with external systems.

## Documentation

### Technical Documentation (`docs/`)

Contains architectural decisions, design documents, and technical specifications.

### API Documentation

Generated from docstrings and OpenAPI specification via FastAPI.

## Modular Monolith Structure

Per the selected architecture decision (docs/creative-phase-architecture.md), the project uses a **Modular Monolith** approach:

- All monitoring modules live within one FastAPI application under the `monitors/` directory.
- Modules are imported as separate routers in `src/stream_health_monitor/api/app.py`.
- Docker entry-point sets up the FastAPI server with routes for each module.
- Feature flags via environment variables allow enabling/disabling modules on startup. 