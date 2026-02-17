#!/usr/bin/env python3
"""Agent-core typed chat vertical slice over the IPC hub."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

import websockets

from contract import ContractError, build_chat_assistant_payload, validate_chat_user_message
from failure_templates import failure_message
from planner import propose_plan
from tasksprite_common import get_service_logger, new_trace_id

HUB_URL = 'ws://127.0.0.1:17171/ws'
SERVICE_NAME = 'agent-core'


class AgentCoreClient:
    def __init__(self) -> None:
        self._logger = get_service_logger(SERVICE_NAME)

    async def run_forever(self) -> None:
        while True:
            try:
                await self._run_session()
            except Exception as err:  # broad catch keeps service alive in dev stage
                self._logger.event(logging.ERROR, 'session.error', new_trace_id(), error=str(err))
                await asyncio.sleep(2)

    async def _run_session(self) -> None:
        async with websockets.connect(HUB_URL, ping_interval=None) as socket:
            auth_trace = new_trace_id()
            await socket.send(
                json.dumps(
                    self._build_envelope(
                        target='ipc-hub',
                        topic='auth.hello',
                        trace_id=auth_trace,
                        payload={
                            'service': SERVICE_NAME,
                            'token': 'dev-token',
                            'capabilities': ['chat.assistant_message']
                        }
                    )
                )
            )
            self._logger.event(logging.INFO, 'auth.sent', auth_trace, hub_url=HUB_URL)
            heartbeat_task = asyncio.create_task(self._heartbeat_loop(socket))
            try:
                async for raw in socket:
                    await self._handle_message(socket, raw)
            finally:
                heartbeat_task.cancel()

    async def _handle_message(self, socket: websockets.WebSocketClientProtocol, raw: str) -> None:
        envelope = json.loads(raw)
        topic = envelope.get('topic')
        trace_id = envelope.get('trace_id', new_trace_id())

        if topic == 'auth.ok':
            self._logger.event(logging.INFO, 'auth.ok', trace_id)
            return

        if topic == 'chat.user_message':
            try:
                user_text = validate_chat_user_message(envelope)
                plan = propose_plan(user_text)
                if plan:
                    response = self._build_envelope(
                        target='desktop-ui',
                        topic='chat.assistant_plan',
                        trace_id=trace_id,
                        payload=plan,
                        reply_to=envelope.get('id')
                    )
                    await socket.send(json.dumps(response))
                    self._logger.event(logging.INFO, 'chat.plan', trace_id, tools=len(plan.get('proposed_tools', [])))
                    return

                assistant_text = self._build_reply(user_text)
                assistant_payload = build_chat_assistant_payload(assistant_text)
            except ContractError as err:
                assistant_payload = build_chat_assistant_payload(failure_message(err.code, err.message))

            response = self._build_envelope(
                target='desktop-ui',
                topic='chat.assistant_message',
                trace_id=trace_id,
                payload=assistant_payload,
                reply_to=envelope.get('id')
            )
            await socket.send(json.dumps(response))
            self._logger.event(
                logging.INFO,
                'chat.replied',
                trace_id,
                input_chars=len(user_text) if 'user_text' in locals() else 0
            )
            return

        if topic == 'hb.pong':
            return

        if topic.startswith('chat.') and envelope.get('from') == 'desktop-ui':
            fallback = build_chat_assistant_payload(
                failure_message('ERR_TOPIC_MISMATCH', f'unsupported topic {topic}')
            )
            response = self._build_envelope(
                target='desktop-ui',
                topic='chat.assistant_message',
                trace_id=trace_id,
                payload=fallback,
                reply_to=envelope.get('id')
            )
            await socket.send(json.dumps(response))
            return

        self._logger.event(logging.INFO, 'message.ignored', trace_id, topic=str(topic))

    async def _heartbeat_loop(self, socket: websockets.WebSocketClientProtocol) -> None:
        while True:
            await asyncio.sleep(5)
            if socket.closed:
                return
            await socket.send(
                json.dumps(
                    self._build_envelope(
                        target='ipc-hub',
                        topic='hb.ping',
                        trace_id=new_trace_id(),
                        payload={'source': SERVICE_NAME}
                    )
                )
            )

    def _build_reply(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return 'I received an empty message. Please send text to continue.'
        return f'Stub reply from agent-core: {text}'

    def _build_envelope(
        self,
        target: str,
        topic: str,
        trace_id: str,
        payload: dict[str, Any],
        reply_to: str | None = None
    ) -> dict[str, Any]:
        return {
            'v': 1,
            'id': new_trace_id(),
            'ts': datetime.now(timezone.utc).isoformat(),
            'from': SERVICE_NAME,
            'to': target,
            'topic': topic,
            'reply_to': reply_to,
            'trace_id': trace_id,
            'payload': payload
        }


async def main() -> None:
    logger = get_service_logger(SERVICE_NAME)
    logger.event(logging.INFO, 'service.start', new_trace_id(), mode='typed-chat-v0')
    await AgentCoreClient().run_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
