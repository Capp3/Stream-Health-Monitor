"""
FastAPI application for the Stream Health Monitor.

This module defines the main FastAPI application and its routes.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_wsgi_app
from prometheus_client.exposition import _ThreadingSimpleServer
from prometheus_client.registry import REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from stream_health_monitor.config.loader import load_config
from stream_health_monitor.db.metrics import setup_metrics

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Load configuration
    config = load_config()

    # Set up metrics registry
    setup_metrics(REGISTRY)

    # Create FastAPI app
    app = FastAPI(
        title="Stream Health Monitor",
        description="A monitoring system for video streams",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Set up routes
    @app.get("/")
    def root():
        """Root endpoint."""
        return {"message": "Stream Health Monitor API"}

    @app.get("/health")
    def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/api/v1/status")
    def status():
        """System status endpoint."""
        # In the future, this would return actual system status
        return {
            "status": "ok",
            "monitors": {
                "web_presenter": True,
                "vimeo": True,
                "ffprobe": True,
                "network": True,
            },
        }

    # Set up error handlers
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle all unhandled exceptions."""
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    # Set up Prometheus metrics endpoint
    @app.on_event("startup")
    async def startup_prometheus_server():
        """Start Prometheus metrics server on a separate port."""
        # Create WSGI app for Prometheus metrics
        metrics_app = make_wsgi_app(REGISTRY)

        # Create dispatcher middleware (allows mounting the metrics app)
        app_dispatch = DispatcherMiddleware(app, {"/metrics": metrics_app})

        # Start metrics server in a separate thread
        metrics_port = config.get("metrics_port", 8001)
        metrics_server = _ThreadingSimpleServer(("0.0.0.0", metrics_port), app_dispatch)
        metrics_server.daemon = True
        metrics_server.start()
        logger.info(f"Prometheus metrics available at http://0.0.0.0:{metrics_port}/metrics")

    return app
