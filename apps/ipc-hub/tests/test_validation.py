import unittest

from ipc_hub.validation import ValidationError, validate_envelope


class ValidationTests(unittest.TestCase):
    def _base_message(self):
        return {
            'v': 1,
            'id': 'id-1',
            'ts': '2026-02-16T00:00:00Z',
            'from': 'desktop-ui',
            'to': 'agent-core',
            'topic': 'chat.user_message',
            'reply_to': None,
            'trace_id': 'trace-1',
            'payload': {'text': 'hi'}
        }

    def test_validate_envelope_success(self):
        msg = self._base_message()
        self.assertEqual(validate_envelope(msg), msg)

    def test_missing_key_rejected(self):
        msg = self._base_message()
        del msg['topic']
        with self.assertRaises(ValidationError) as err:
            validate_envelope(msg)
        self.assertEqual(err.exception.code, 'ERR_MISSING_KEYS')

    def test_unsupported_version_rejected(self):
        msg = self._base_message()
        msg['v'] = 2
        with self.assertRaises(ValidationError) as err:
            validate_envelope(msg)
        self.assertEqual(err.exception.code, 'ERR_UNSUPPORTED_VERSION')

    def test_payload_must_be_object(self):
        msg = self._base_message()
        msg['payload'] = []
        with self.assertRaises(ValidationError) as err:
            validate_envelope(msg)
        self.assertEqual(err.exception.code, 'ERR_INVALID_PAYLOAD')


if __name__ == '__main__':
    unittest.main()
