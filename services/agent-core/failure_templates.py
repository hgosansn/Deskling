"""Failure response templates for agent-core with retry suggestions."""

from __future__ import annotations


def failure_message(error_code: str, detail: str = '') -> str:
    templates = {
        'ERR_EMPTY_TEXT': 'No message content detected. Retry: type a short request, for example "open calculator".',
        'ERR_TEXT_TOO_LONG': 'Message is too long. Retry: send a shorter request under 4000 characters.',
        'ERR_TOPIC_MISMATCH': 'Unsupported topic received. Retry: send topic chat.user_message.',
        'ERR_INVALID_TEXT': 'Invalid message payload. Retry: ensure payload.text is a string.'
    }

    base = templates.get(error_code, 'Request could not be processed. Retry: rephrase your request and try again.')
    if detail:
        return f'{base} (detail: {detail})'
    return base
