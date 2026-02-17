import unittest

from ipc_hub.router import MessageRouter
from ipc_hub.validation import ValidationError


class RouterTests(unittest.TestCase):
    def _message(self, target='agent-core'):
        return {
            'v': 1,
            'id': 'id-1',
            'ts': '2026-02-16T00:00:00Z',
            'from': 'desktop-ui',
            'to': target,
            'topic': 'chat.user_message',
            'reply_to': None,
            'trace_id': 'trace-1',
            'payload': {'text': 'hello'}
        }

    def test_route_enqueues_for_registered_destination(self):
        router = MessageRouter()
        router.register('agent-core')

        result = router.route(self._message())

        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['queue_size'], 1)
        self.assertEqual(router.drain('agent-core')[0]['topic'], 'chat.user_message')

    def test_route_rejects_unknown_destination(self):
        router = MessageRouter()
        with self.assertRaises(ValidationError) as err:
            router.route(self._message(target='unknown'))
        self.assertEqual(err.exception.code, 'ERR_UNKNOWN_DESTINATION')


if __name__ == '__main__':
    unittest.main()
