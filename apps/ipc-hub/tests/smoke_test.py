#!/usr/bin/env python3
"""Smoke test for minimal envelope validation and routing."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ipc_hub import MessageRouter


def build_message(topic: str, target: str) -> dict[str, object]:
    return {
        'v': 1,
        'id': uuid4().hex,
        'ts': datetime.now(timezone.utc).isoformat(),
        'from': 'desktop-ui',
        'to': target,
        'topic': topic,
        'reply_to': None,
        'trace_id': uuid4().hex,
        'payload': {'text': 'hello'}
    }


def main() -> None:
    router = MessageRouter()
    router.register('agent-core')

    result = router.route(build_message('chat.user_message', 'agent-core'))
    assert result['status'] == 'ok'
    assert result['queued_for'] == 'agent-core'

    drained = router.drain('agent-core')
    assert len(drained) == 1
    assert drained[0]['topic'] == 'chat.user_message'

    print('smoke test passed: envelope validation and routing are functional')


if __name__ == '__main__':
    main()
