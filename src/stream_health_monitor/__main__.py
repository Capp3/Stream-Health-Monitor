"""
Main entry point for the Stream Health Monitor.

This module allows running the monitoring service directly with `python -m stream_health_monitor`.
"""

import argparse
import logging
import sys

from stream_health_monitor.api.app import create_app


def setup_logging(level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/stream_health_monitor.log"),
        ],
    )


def main():
    """Run the Stream Health Monitor application."""
    parser = argparse.ArgumentParser(description="Stream Health Monitor")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the API server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the API server")
    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)

    # Create and run the FastAPI app
    app = create_app()

    # Using uvicorn here directly to avoid adding it as a hard dependency
    # Usually this would be run with `uvicorn stream_health_monitor.api.app:app --host 0.0.0.0 --port 8000`
    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
