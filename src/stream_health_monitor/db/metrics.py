"""
Metrics schema and storage for the Stream Health Monitor.

This module defines the Prometheus metrics used by the application.
"""

import logging
from typing import Dict

from prometheus_client import Counter, Gauge, Info
from prometheus_client.registry import CollectorRegistry

logger = logging.getLogger(__name__)

# Define metrics
stream_status = Gauge(
    "stream_health_stream_status",
    "Stream online status (1=online, 0=offline)",
    ["stream_name", "stream_type"],
)

stream_bitrate = Gauge(
    "stream_health_stream_bitrate",
    "Stream bitrate in bits per second",
    ["stream_name", "stream_type"],
)

stream_health_score = Gauge(
    "stream_health_score",
    "Overall health score for a stream (0-100)",
    ["stream_name", "stream_type"],
)

stream_packet_loss = Gauge(
    "stream_health_packet_loss",
    "Stream packet loss percentage",
    ["stream_name", "stream_type"],
)

stream_latency = Gauge(
    "stream_health_latency",
    "Stream latency in milliseconds",
    ["stream_name", "stream_type"],
)

network_ping_latency = Gauge(
    "stream_health_network_ping_latency",
    "Network ping latency in milliseconds",
    ["target"],
)

network_packet_loss = Gauge(
    "stream_health_network_packet_loss",
    "Network packet loss percentage",
    ["target"],
)

# Monitoring system info
system_info = Info(
    "stream_health_system_info",
    "Information about the Stream Health Monitor system",
)

# Error counts
error_counter = Counter(
    "stream_health_errors_total",
    "Total number of errors encountered",
    ["stream_name", "stream_type", "error_type"],
)


def setup_metrics(registry: CollectorRegistry) -> None:
    """
    Set up metrics in the provided registry.

    Args:
        registry: Prometheus collector registry
    """
    # Register all metrics with the provided registry
    registry.register(stream_status)
    registry.register(stream_bitrate)
    registry.register(stream_health_score)
    registry.register(stream_packet_loss)
    registry.register(stream_latency)
    registry.register(network_ping_latency)
    registry.register(network_packet_loss)
    registry.register(system_info)
    registry.register(error_counter)

    # Set system info
    system_info.info({
        "version": "0.1.0",
        "system": "Stream Health Monitor",
    })

    logger.info("Metrics initialized")


def calculate_health_score(metrics: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate a health score based on weighted metrics.

    This implements the Weighted Sum of Normalized Metrics algorithm.
    Each metric is normalized to a 0-1 scale, multiplied by its weight,
    and summed to produce a final score in the range 0-100.

    Args:
        metrics: Dictionary of metric names and values
        weights: Dictionary of metric names and weights (0-1)

    Returns:
        float: Health score (0-100)
    """
    if not metrics or not weights:
        return 0.0

    # Default normalization functions for known metrics
    normalizers = {
        "status": lambda x: 1.0 if x > 0 else 0.0,  # 1 = online, 0 = offline
        "bitrate": lambda x, target=5000000: min(x / target, 1.0),  # Normalize to target bitrate
        "packet_loss": lambda x: 1.0 - min(x / 100.0, 1.0),  # Invert percentage
        "latency": lambda x, max_ms=1000: 1.0 - min(x / max_ms, 1.0),  # Invert and normalize
    }

    # Calculate weighted score
    score = 0.0
    total_weight = 0.0

    for metric_name, metric_value in metrics.items():
        if metric_name in weights:
            weight = weights[metric_name]
            normalizer = normalizers.get(metric_name, lambda x: x)

            # Normalize metric to 0-1 scale
            normalized_value = normalizer(metric_value)

            # Add weighted contribution
            score += normalized_value * weight
            total_weight += weight

    # Scale to 0-100 range
    if total_weight > 0:
        final_score = (score / total_weight) * 100
    else:
        final_score = 0.0

    return final_score
