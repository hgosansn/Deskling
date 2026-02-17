"""Heuristic planner for initial chat.assistant_plan output with risk labels."""

from __future__ import annotations

from typing import Any
from uuid import uuid4


def propose_plan(user_text: str) -> dict[str, Any] | None:
    text = user_text.lower()
    tools: list[dict[str, Any]] = []

    if 'notify' in text:
        tools.append({'name': 'notify.send', 'risk': 'low', 'reason': 'user asked for notification'})

    if 'open ' in text or 'launch ' in text:
        tools.append({'name': 'apps.open', 'risk': 'low', 'reason': 'user asked to open an app'})

    if 'write ' in text or 'create file' in text:
        tools.append({'name': 'files.write_text', 'risk': 'medium', 'reason': 'request mutates local files'})

    if 'delete ' in text or 'remove ' in text:
        tools.append({'name': 'files.delete_path', 'risk': 'high', 'reason': 'destructive file operation'})

    if not tools:
        return None

    needs_confirmation = any(tool['risk'] in ('medium', 'high') for tool in tools)
    summary = 'Proposed tool-assisted plan based on your request.'

    proposed_calls = [
        {
            'call_id': f'call_{uuid4().hex[:10]}',
            'tool_name': tool['name'],
            'args': {'source': 'planner_v0'},
            'confirmation_required': tool['risk'] in ('medium', 'high'),
            'risk': tool['risk']
        }
        for tool in tools
    ]

    return {
        'summary': summary,
        'needs_confirmation': needs_confirmation,
        'proposed_tools': tools,
        'proposed_calls': proposed_calls
    }
