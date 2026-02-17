"""Logging utilities with trace ID support."""

import logging
import sys
from typing import Optional
from ulid import ULID


class TraceIDFilter(logging.Filter):
    """Add trace_id to log records if available in context."""

    def filter(self, record):
        if not hasattr(record, 'trace_id'):
            record.trace_id = '-'
        return True


def setup_logger(
    name: str,
    level: str = "INFO",
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with trace ID support.

    Args:
        name: Logger name (typically service name)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Optional custom format string

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))

    # Default format with trace ID
    if log_format is None:
        log_format = (
            '%(asctime)s | %(name)s | %(levelname)s | '
            'trace_id=%(trace_id)s | %(message)s'
        )

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    handler.addFilter(TraceIDFilter())

    logger.addHandler(handler)
    return logger


def generate_trace_id() -> str:
    """
    Generate a new ULID trace ID.

    Returns:
        String representation of ULID
    """
    return str(ULID())


def log_with_trace(logger: logging.Logger, level: str, message: str, trace_id: str):
    """
    Log a message with an explicit trace ID.

    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        trace_id: Trace ID to include
    """
    log_func = getattr(logger, level.lower())
    log_func(message, extra={'trace_id': trace_id})
