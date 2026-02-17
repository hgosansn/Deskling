"""Agent-core message contract helpers for IPC topics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ContractError(Exception):
    code: str
    message: str


def validate_chat_user_message(envelope: dict[str, Any]) -> str:
    if envelope.get('topic') != 'chat.user_message':
        raise ContractError('ERR_TOPIC_MISMATCH', 'expected topic chat.user_message')

    payload = envelope.get('payload')
    if not isinstance(payload, dict):
        raise ContractError('ERR_INVALID_PAYLOAD', 'payload must be an object')

    text = payload.get('text')
    if not isinstance(text, str):
        raise ContractError('ERR_INVALID_TEXT', 'payload.text must be a string')

    normalized = text.strip()
    if len(normalized) == 0:
        raise ContractError('ERR_EMPTY_TEXT', 'payload.text must be non-empty')

    if len(normalized) > 4000:
        raise ContractError('ERR_TEXT_TOO_LONG', 'payload.text exceeds 4000 characters')

    return normalized


def build_chat_assistant_payload(text: str) -> dict[str, str]:
    normalized = text.strip()
    if len(normalized) == 0:
        raise ContractError('ERR_EMPTY_TEXT', 'assistant text must be non-empty')
    if len(normalized) > 4000:
        raise ContractError('ERR_TEXT_TOO_LONG', 'assistant text exceeds 4000 characters')
    return {'text': normalized}
