#!/usr/bin/env python3
"""WebSocket IPC hub baseline with loopback-only binding and basic routing."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import websockets
from websockets.server import WebSocketServerProtocol

from ipc_hub.validation import ValidationError, validate_envelope
from tasksprite_common import get_service_logger, new_trace_id

HOST = '127.0.0.1'
PORT = 17171
PATH = '/ws'
AUTH_TOKEN = os.getenv('TASKSPRITE_IPC_TOKEN', 'dev-token')
HEARTBEAT_TIMEOUT_SECONDS = 20


@dataclass
class ClientSession:
    service_name: str
    websocket: WebSocketServerProtocol
    last_seen_monotonic: float


class IpcHubServer:
    def __init__(self) -> None:
        self._clients: dict[str, ClientSession] = {}
        self._logger = get_service_logger('ipc-hub')

    async def run(self) -> None:
        self._logger.event(logging.INFO, 'hub.start', new_trace_id(), bind=HOST, port=PORT, path=PATH)
        monitor_task = asyncio.create_task(self._monitor_heartbeats())
        try:
            async with websockets.serve(self._handle_connection, HOST, PORT, ping_interval=None):
                await asyncio.Future()
        finally:
            monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await monitor_task

    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        if path != PATH:
            await websocket.close(code=1008, reason='invalid_path')
            return

        session: ClientSession | None = None

        try:
            raw_first = await websocket.recv()
            first_message = json.loads(raw_first)
            validated = validate_envelope(first_message)

            if validated['topic'] != 'auth.hello':
                raise ValidationError('ERR_AUTH_REQUIRED', 'first message must be auth.hello')
            session = self._create_session_from_auth(validated, websocket)
            self._clients[session.service_name] = session

            await self._send_auth_ok(websocket, validated)
            self._logger.event(logging.INFO, 'auth.ok', validated['trace_id'], client_service=session.service_name)

            async for raw_message in websocket:
                try:
                    await self._handle_message(session, raw_message)
                except ValidationError as err:
                    await self._send_error(websocket, err, trace_id=new_trace_id(), target=session.service_name)
                    self._logger.event(
                        logging.WARNING,
                        'message.rejected',
                        new_trace_id(),
                        client_service=session.service_name,
                        code=err.code,
                        reason=err.message
                    )
        except (json.JSONDecodeError, ValidationError) as err:
            if isinstance(err, ValidationError):
                await self._send_error(websocket, err, trace_id=new_trace_id(), target='unknown')
                self._logger.event(logging.WARNING, 'message.invalid', new_trace_id(), code=err.code, reason=err.message)
            else:
                parse_error = ValidationError('ERR_INVALID_JSON', 'message must be valid JSON')
                await self._send_error(websocket, parse_error, trace_id=new_trace_id(), target='unknown')
                self._logger.event(logging.WARNING, 'message.invalid_json', new_trace_id())
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if session and self._clients.get(session.service_name) is session:
                self._clients.pop(session.service_name, None)
                self._logger.event(logging.INFO, 'client.disconnected', new_trace_id(), client_service=session.service_name)

    async def _handle_message(self, session: ClientSession, raw_message: str) -> None:
        envelope = validate_envelope(json.loads(raw_message))
        session.last_seen_monotonic = asyncio.get_running_loop().time()

        topic = envelope['topic']
        trace_id = envelope['trace_id']

        if topic == 'hb.ping':
            await session.websocket.send(json.dumps(self._build_envelope('ipc-hub', session.service_name, 'hb.pong', trace_id, {})))
            return

        target_name = envelope['to']
        target = self._clients.get(target_name)

        if not target:
            raise ValidationError('ERR_UNKNOWN_DESTINATION', f'unknown destination service: {target_name}')

        await target.websocket.send(json.dumps(envelope))
        self._logger.event(
            logging.INFO,
            'route.forwarded',
            trace_id,
            from_service=session.service_name,
            to_service=target_name,
            topic=topic,
            reply_to=envelope.get('reply_to')
        )

    async def _send_auth_ok(self, websocket: WebSocketServerProtocol, incoming: dict[str, Any]) -> None:
        response = self._build_envelope(
            sender='ipc-hub',
            target=incoming['from'],
            topic='auth.ok',
            trace_id=incoming['trace_id'],
            payload={'service': incoming['from']},
            reply_to=incoming['id']
        )
        await websocket.send(json.dumps(response))

    def _create_session_from_auth(self, validated: dict[str, Any], websocket: WebSocketServerProtocol) -> ClientSession:
        auth_payload = validated.get('payload') or {}
        if auth_payload.get('token') != AUTH_TOKEN:
            raise ValidationError('ERR_AUTH_INVALID', 'invalid auth token')

        service_name = str(validated['from'])
        return ClientSession(
            service_name=service_name,
            websocket=websocket,
            last_seen_monotonic=asyncio.get_running_loop().time()
        )

    async def _send_error(
        self,
        websocket: WebSocketServerProtocol,
        error: ValidationError,
        trace_id: str,
        target: str
    ) -> None:
        payload = error.to_error_payload()
        response = self._build_envelope(
            sender='ipc-hub',
            target=target,
            topic='ipc.error',
            trace_id=trace_id,
            payload=payload
        )
        await websocket.send(json.dumps(response))

    def _build_envelope(
        self,
        sender: str,
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
            'from': sender,
            'to': target,
            'topic': topic,
            'reply_to': reply_to,
            'trace_id': trace_id,
            'payload': payload
        }

    async def _monitor_heartbeats(self) -> None:
        loop = asyncio.get_running_loop()
        while True:
            await asyncio.sleep(5)
            await self._expire_stale_clients(loop.time())

    async def _expire_stale_clients(self, now: float) -> None:
        stale = [
            session for session in self._clients.values()
            if (now - session.last_seen_monotonic) > HEARTBEAT_TIMEOUT_SECONDS
        ]
        for session in stale:
            self._logger.event(
                logging.WARNING,
                'client.timeout',
                new_trace_id(),
                client_service=session.service_name,
                timeout_seconds=HEARTBEAT_TIMEOUT_SECONDS
            )
            await session.websocket.close(code=1001, reason='heartbeat_timeout')
            self._clients.pop(session.service_name, None)


async def main() -> None:
    server = IpcHubServer()
    await server.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
