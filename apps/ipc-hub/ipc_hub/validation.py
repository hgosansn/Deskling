"""Minimal envelope validation for IPC messages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_KEYS = {'v', 'id', 'ts', 'from', 'to', 'topic', 'reply_to', 'trace_id', 'payload'}
SUPPORTED_VERSION = 1


@dataclass
class ValidationError(Exception):
    code: str
    message: str

    def to_error_payload(self) -> dict[str, str]:
        return {'code': self.code, 'message': self.message}


def validate_envelope(message: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_KEYS if key not in message]
    if missing:
        raise ValidationError('ERR_MISSING_KEYS', f'missing required keys: {", ".join(sorted(missing))}')

    if message.get('v') != SUPPORTED_VERSION:
        raise ValidationError('ERR_UNSUPPORTED_VERSION', f'unsupported envelope version: {message.get("v")}')

    if not isinstance(message.get('payload'), dict):
        raise ValidationError('ERR_INVALID_PAYLOAD', 'payload must be a JSON object')

    for key in ('id', 'trace_id', 'from', 'to', 'topic', 'ts'):
        value = message.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValidationError('ERR_INVALID_FIELD', f'field {key} must be a non-empty string')

    return message
