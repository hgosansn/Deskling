import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'agent-core'))

from contract import ContractError, build_chat_assistant_payload, validate_chat_user_message  # noqa: E402


class ContractTests(unittest.TestCase):
    def test_validate_chat_user_message_success(self):
        text = validate_chat_user_message({'topic': 'chat.user_message', 'payload': {'text': ' hi '}})
        self.assertEqual(text, 'hi')

    def test_validate_chat_user_message_rejects_empty(self):
        with self.assertRaises(ContractError) as err:
            validate_chat_user_message({'topic': 'chat.user_message', 'payload': {'text': '  '}})
        self.assertEqual(err.exception.code, 'ERR_EMPTY_TEXT')

    def test_validate_chat_user_message_rejects_wrong_topic(self):
        with self.assertRaises(ContractError) as err:
            validate_chat_user_message({'topic': 'hb.ping', 'payload': {'text': 'x'}})
        self.assertEqual(err.exception.code, 'ERR_TOPIC_MISMATCH')

    def test_build_chat_assistant_payload(self):
        self.assertEqual(build_chat_assistant_payload('hello'), {'text': 'hello'})

    def test_build_chat_assistant_payload_rejects_empty(self):
        with self.assertRaises(ContractError):
            build_chat_assistant_payload('')


if __name__ == '__main__':
    unittest.main()
