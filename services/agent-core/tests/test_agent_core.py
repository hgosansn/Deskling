import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'agent-core'))

import main as agent_main  # noqa: E402


class FakeSocket:
    def __init__(self):
        self.sent = []

    async def send(self, raw):
        self.sent.append(json.loads(raw))


class AgentCoreTests(unittest.IsolatedAsyncioTestCase):
    async def test_user_message_generates_assistant_reply(self):
        client = agent_main.AgentCoreClient()
        socket = FakeSocket()

        message = {
            'id': 'id-1',
            'topic': 'chat.user_message',
            'trace_id': 'trace-1',
            'payload': {'text': 'hello deskling'}
        }

        await client._handle_message(socket, json.dumps(message))

        self.assertEqual(socket.sent[0]['topic'], 'chat.assistant_message')
        self.assertEqual(socket.sent[0]['trace_id'], 'trace-1')
        self.assertEqual(socket.sent[0]['reply_to'], 'id-1')
        self.assertIn('Stub reply from agent-core', socket.sent[0]['payload']['text'])

    async def test_empty_message_returns_guidance(self):
        client = agent_main.AgentCoreClient()
        socket = FakeSocket()

        message = {
            'id': 'id-1',
            'topic': 'chat.user_message',
            'trace_id': 'trace-2',
            'payload': {'text': '   '}
        }

        await client._handle_message(socket, json.dumps(message))
        self.assertIn('retry:', socket.sent[0]['payload']['text'].lower())

    async def test_tool_intent_returns_assistant_plan(self):
        client = agent_main.AgentCoreClient()
        socket = FakeSocket()

        message = {
            'id': 'id-2',
            'topic': 'chat.user_message',
            'trace_id': 'trace-3',
            'payload': {'text': 'delete this file'}
        }

        await client._handle_message(socket, json.dumps(message))

        self.assertEqual(socket.sent[0]['topic'], 'chat.assistant_plan')
        self.assertEqual(socket.sent[0]['trace_id'], 'trace-3')
        self.assertTrue(socket.sent[0]['payload']['needs_confirmation'])
        risks = [tool['risk'] for tool in socket.sent[0]['payload']['proposed_tools']]
        self.assertIn('high', risks)

    async def test_unknown_chat_topic_returns_retry_message(self):
        client = agent_main.AgentCoreClient()
        socket = FakeSocket()

        message = {
            'id': 'id-3',
            'topic': 'chat.unknown',
            'trace_id': 'trace-4',
            'from': 'desktop-ui',
            'payload': {'text': 'x'}
        }

        await client._handle_message(socket, json.dumps(message))

        self.assertEqual(socket.sent[0]['topic'], 'chat.assistant_message')
        self.assertIn('Retry:', socket.sent[0]['payload']['text'])


if __name__ == '__main__':
    unittest.main()
