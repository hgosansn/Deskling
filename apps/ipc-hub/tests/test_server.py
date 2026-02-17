import asyncio
import json
import unittest

from ipc_hub.validation import ValidationError
from server import ClientSession, IpcHubServer


class FakeSocket:
    def __init__(self):
        self.sent = []
        self.closed = None

    async def send(self, raw):
        self.sent.append(json.loads(raw))

    async def close(self, code, reason):
        self.closed = {'code': code, 'reason': reason}


class ServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_send_auth_ok_envelope(self):
        server = IpcHubServer()
        socket = FakeSocket()

        await server._send_auth_ok(
            socket,
            {
                'from': 'desktop-ui',
                'id': 'msg-1',
                'trace_id': 'trace-1'
            }
        )

        self.assertEqual(socket.sent[0]['topic'], 'auth.ok')
        self.assertEqual(socket.sent[0]['reply_to'], 'msg-1')
        self.assertEqual(socket.sent[0]['trace_id'], 'trace-1')

    async def test_create_session_requires_valid_token(self):
        server = IpcHubServer()
        socket = FakeSocket()

        with self.assertRaises(ValidationError) as err:
            server._create_session_from_auth(
                {
                    'from': 'desktop-ui',
                    'payload': {'token': 'bad-token'}
                },
                socket
            )
        self.assertEqual(err.exception.code, 'ERR_AUTH_INVALID')

    async def test_handle_message_forwards_to_destination(self):
        server = IpcHubServer()
        source_ws = FakeSocket()
        target_ws = FakeSocket()

        source = ClientSession('desktop-ui', source_ws, asyncio.get_running_loop().time())
        target = ClientSession('agent-core', target_ws, asyncio.get_running_loop().time())
        server._clients['desktop-ui'] = source
        server._clients['agent-core'] = target

        envelope = {
            'v': 1,
            'id': 'id-1',
            'ts': '2026-02-16T00:00:00Z',
            'from': 'desktop-ui',
            'to': 'agent-core',
            'topic': 'chat.user_message',
            'reply_to': None,
            'trace_id': 'trace-1',
            'payload': {'text': 'hello'}
        }

        await server._handle_message(source, json.dumps(envelope))

        self.assertEqual(target_ws.sent[0]['topic'], 'chat.user_message')
        self.assertEqual(target_ws.sent[0]['trace_id'], 'trace-1')

    async def test_ping_returns_pong(self):
        server = IpcHubServer()
        source_ws = FakeSocket()
        source = ClientSession('desktop-ui', source_ws, asyncio.get_running_loop().time())

        ping = {
            'v': 1,
            'id': 'id-1',
            'ts': '2026-02-16T00:00:00Z',
            'from': 'desktop-ui',
            'to': 'ipc-hub',
            'topic': 'hb.ping',
            'reply_to': None,
            'trace_id': 'trace-2',
            'payload': {}
        }

        await server._handle_message(source, json.dumps(ping))
        self.assertEqual(source_ws.sent[0]['topic'], 'hb.pong')
        self.assertEqual(source_ws.sent[0]['trace_id'], 'trace-2')

    async def test_expire_stale_clients(self):
        server = IpcHubServer()
        stale_ws = FakeSocket()
        fresh_ws = FakeSocket()

        server._clients['stale'] = ClientSession('stale', stale_ws, 1.0)
        server._clients['fresh'] = ClientSession('fresh', fresh_ws, 100.0)

        await server._expire_stale_clients(100.0)

        self.assertNotIn('stale', server._clients)
        self.assertIn('fresh', server._clients)
        self.assertEqual(stale_ws.closed['reason'], 'heartbeat_timeout')


if __name__ == '__main__':
    unittest.main()
