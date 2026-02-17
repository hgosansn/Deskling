"""Structured logging helpers with trace-id support for TaskSprite services."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            'ts': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname.lower(),
            'service': getattr(record, 'service', record.name),
            'event': record.getMessage(),
            'trace_id': getattr(record, 'trace_id', None)
        }

        fields = getattr(record, 'fields', None)
        if isinstance(fields, dict):
            payload.update(fields)

        return json.dumps(payload, ensure_ascii=True)


class ServiceLogger(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        extra = kwargs.get('extra', {})
        merged_extra = {**self.extra, **extra}
        kwargs['extra'] = merged_extra
        return msg, kwargs

    def event(self, level: int, event: str, trace_id: str, **fields: Any) -> None:
        self.log(level, event, extra={'trace_id': trace_id, 'fields': fields})


_logger_cache: dict[str, ServiceLogger] = {}


def get_service_logger(service_name: str) -> ServiceLogger:
    if service_name in _logger_cache:
        return _logger_cache[service_name]

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    adapter = ServiceLogger(logger, {'service': service_name})
    _logger_cache[service_name] = adapter
    return adapter


def new_trace_id() -> str:
    return uuid4().hex
