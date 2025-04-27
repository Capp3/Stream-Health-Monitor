"""
Configuration loader for the Stream Health Monitor.

This module provides utilities for loading and validating configuration from
YAML files and environment variables.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, validator

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(Path("config/.env"))


class StreamConfig(BaseModel):
    """Configuration for a monitored stream."""

    name: str
    type: str  # web_presenter, vimeo, ffprobe
    url: str
    enabled: bool = True
    polling_interval: int = 30  # seconds

    # Stream-specific settings
    settings: Optional[Dict[str, Any]] = None

    @validator("type")
    def validate_stream_type(cls, v):
        """Validate the stream type."""
        valid_types = ["web_presenter", "vimeo", "ffprobe"]
        if v not in valid_types:
            raise ValueError(f"Stream type must be one of {valid_types}")
        return v


class AlertConfig(BaseModel):
    """Configuration for an alert."""

    name: str
    type: str  # email, webhook, etc.
    enabled: bool = True
    threshold: float = 70.0  # Default health threshold (0-100)

    # Alert-specific settings
    settings: Optional[Dict[str, Any]] = None


class MetricWeight(BaseModel):
    """Weight configuration for a metric in the health score calculation."""

    name: str
    weight: float = 1.0

    @validator("weight")
    def validate_weight(cls, v):
        """Validate the weight is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Weight must be between 0 and 1")
        return v


class Config(BaseModel):
    """Main configuration model."""

    # General settings
    metrics_port: int = 8001  # Port for Prometheus metrics
    log_level: str = "INFO"

    # Monitoring configuration
    streams: Optional[list[StreamConfig]] = None
    alerts: Optional[list[AlertConfig]] = None

    # Health score calculation
    metric_weights: Optional[list[MetricWeight]] = None


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file and environment variables.

    Args:
        config_path: Path to the configuration file

    Returns:
        dict: Merged configuration from file and environment variables
    """
    config_dict = {}

    # Load from YAML file if it exists
    config_file = Path(config_path)
    if config_file.exists():
        try:
            with open(config_file) as f:
                config_dict = yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Error loading configuration from {config_path}: {e}")
    else:
        logger.warning(f"Configuration file {config_path} not found, using defaults")

    # Override with environment variables
    # Environment variables take precedence over YAML configuration
    env_prefix = "STREAM_HEALTH_"
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            # Convert to lowercase and remove prefix
            config_key = key[len(env_prefix) :].lower()
            # Handle nested keys (e.g., STREAM_HEALTH_METRICS_PORT -> metrics_port)
            parts = config_key.split("_")

            # Build nested dictionary
            current_dict = config_dict
            for part in parts[:-1]:
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]

            # Set final value
            current_dict[parts[-1]] = value

    # Validate configuration
    try:
        validated_config = Config(**config_dict)
        return validated_config.dict()
    except ValidationError as e:
        logger.error(f"Configuration validation error: {e}")
        # Return the original dict if validation fails
        return config_dict
