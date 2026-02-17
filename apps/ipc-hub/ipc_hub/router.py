"""Minimal in-memory routing for IPC hub smoke validation."""

from __future__ import annotations

from typing import Any

from .validation import ValidationError, validate_envelope


class MessageRouter:
    def __init__(self) -> None:
        self._queues: dict[str, list[dict[str, Any]]] = {}

    def register(self, service_name: str) -> None:
        if service_name not in self._queues:
            self._queues[service_name] = []

    def route(self, envelope: dict[str, Any]) -> dict[str, Any]:
        validated = validate_envelope(envelope)
        destination = validated['to']

        if destination not in self._queues:
            raise ValidationError('ERR_UNKNOWN_DESTINATION', f'unknown destination service: {destination}')

        self._queues[destination].append(validated)
        return {'status': 'ok', 'queued_for': destination, 'queue_size': len(self._queues[destination])}

    def drain(self, service_name: str) -> list[dict[str, Any]]:
        messages = self._queues.get(service_name, [])
        self._queues[service_name] = []
        return messages
