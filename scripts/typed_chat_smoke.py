#!/usr/bin/env python3
"""End-to-end smoke test for typed chat vertical slice over IPC hub."""

from __future__ import annotations

import asyncio
import json
import os
import signal
from datetime import datetime, timezone
from uuid import uuid4

import websockets


def envelope(topic: str, sender: str, target: str, trace_id: str, payload: dict, reply_to: str | None = None) -> dict:
    return {
        'v': 1,
        'id': uuid4().hex,
        'ts': datetime.now(timezone.utc).isoformat(),
        'from': sender,
        'to': target,
        'topic': topic,
        'reply_to': reply_to,
        'trace_id': trace_id,
        'payload': payload
    }


async def wait_for_topic(socket: websockets.WebSocketClientProtocol, topic: str, timeout: float = 5.0) -> dict:
    async def _recv_until() -> dict:
        while True:
            message = json.loads(await socket.recv())
            if message.get('topic') == topic:
                return message

    return await asyncio.wait_for(_recv_until(), timeout=timeout)


async def run() -> None:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{root}/shared/python:{root}/apps/ipc-hub"

    hub = await asyncio.create_subprocess_exec('python3', f'{root}/apps/ipc-hub/main.py', env=env)
    await asyncio.sleep(0.4)
    agent = await asyncio.create_subprocess_exec('python3', f'{root}/services/agent-core/main.py', env=env)

    try:
        await asyncio.sleep(1.2)

        async with websockets.connect('ws://127.0.0.1:17171/ws', ping_interval=None) as socket:
            auth_trace = uuid4().hex
            await socket.send(
                json.dumps(
                    envelope(
                        'auth.hello',
                        'desktop-ui',
                        'ipc-hub',
                        auth_trace,
                        {'service': 'desktop-ui', 'token': 'dev-token'}
                    )
                )
            )

            auth_ok = await wait_for_topic(socket, 'auth.ok')
            assert auth_ok.get('trace_id') == auth_trace

            chat_trace = uuid4().hex
            user_msg = envelope('chat.user_message', 'desktop-ui', 'agent-core', chat_trace, {'text': 'smoke ping'})
            await socket.send(json.dumps(user_msg))

            reply = await wait_for_topic(socket, 'chat.assistant_message')
            assert reply.get('trace_id') == chat_trace
            text = (reply.get('payload') or {}).get('text', '')
            assert 'Stub reply from agent-core' in text

            print('typed-chat smoke passed')
    finally:
        for proc in (agent, hub):
            if proc.returncode is None:
                proc.send_signal(signal.SIGINT)
                try:
                    await asyncio.wait_for(proc.wait(), timeout=2)
                except asyncio.TimeoutError:
                    if proc.returncode is None:
                        proc.kill()
                        await proc.wait()
                except ProcessLookupError:
                    pass


if __name__ == '__main__':
    asyncio.run(run())
