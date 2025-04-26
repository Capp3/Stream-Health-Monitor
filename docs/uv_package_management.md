# UV Package Management for RTMP_HMonitor

## Overview

RTMP_HMonitor uses [UV](https://github.com/astral-sh/uv) for package management. UV is a modern Python package manager and resolver that's faster and more reliable than pip. It's designed to be mostly compatible with pip, but with significantly better performance and dependency resolution.

## Key Benefits

- **Speed**: UV installs packages up to 10-100x faster than pip
- **Reliable Resolution**: Better dependency resolution to avoid conflicts
- **Isolated Builds**: Builds packages in isolation to avoid contamination
- **Deterministic Builds**: Produces the same environment every time
- **Compatibility**: Works with existing requirements.txt files

## Project Structure

The project uses a structured approach to dependency management:

```
requirements/
├── production.txt   # Core dependencies needed in production
└── development.txt  # Additional dependencies for development
```

The `development.txt` file includes all production dependencies plus additional tools for testing, linting, and development.

## Setting Up Your Environment

### Automated Setup (Recommended)

We provide a script that automates the environment setup process:

```bash
# Make the script executable if needed
chmod +x scripts/setup_environment.sh

# Run the setup script
./scripts/setup_environment.sh
```

This script will:
1. Install UV if not already installed
2. Create a virtual environment (.venv)
3. Install all development dependencies
4. Create a .env file from .env.sample if needed

### Manual Setup

If you prefer to set up manually or are experiencing issues with the script:

1. Install UV
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a virtual environment
   ```bash
   uv venv .venv
   ```

3. Activate the environment
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate     # On Windows
   ```

4. Install dependencies
   - For development:
     ```bash
     uv pip install -r requirements/development.txt
     ```
   - For production only:
     ```bash
     uv pip install -r requirements/production.txt
     ```

## Daily Workflow

### Activating the Environment

Always activate the virtual environment before working on the project:

```bash
source .venv/bin/activate  # On Linux/macOS
.venv\Scripts\activate     # On Windows
```

### Adding New Dependencies

When adding new dependencies to the project:

1. Add the package to the appropriate requirements file:
   - `requirements/production.txt` for core dependencies
   - `requirements/development.txt` for dev-only dependencies

2. Install the new dependency:
   ```bash
   uv pip install -r requirements/development.txt
   ```

### Updating Dependencies

To update all dependencies to their latest compatible versions:

```bash
uv pip sync requirements/development.txt
```

## Docker Integration

When using Docker, UV is integrated into the build process:

```dockerfile
# Example from Dockerfile
FROM python:3.10-slim

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with UV
COPY requirements/production.txt /app/requirements/
RUN uv pip install -r /app/requirements/production.txt

# Rest of Dockerfile...
```

## CI/CD Integration

For CI/CD pipelines, use UV to install dependencies for faster builds:

```yaml
# Example CI step
- name: Install dependencies
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r requirements/development.txt
```

## Troubleshooting

### Common Issues

1. **UV not found in PATH**: After installation, you may need to restart your terminal or add UV to your PATH manually
2. **Dependency conflicts**: If you encounter conflicts, try removing the virtual environment and creating a new one
3. **Permission issues**: On Linux/macOS, you may need to use `sudo` for the installation or fix directory permissions

### Getting Help

If you encounter any issues with UV:
- Check the [UV documentation](https://github.com/astral-sh/uv)
- Run `uv --help` for command-line help
- File an issue in our project repository 