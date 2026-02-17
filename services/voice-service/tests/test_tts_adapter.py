import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'voice-service'))

from tts_adapter import TtsAdapter, TtsError  # noqa: E402


class TtsAdapterTests(unittest.TestCase):
    def test_mock_synthesize(self):
        adapter = TtsAdapter(provider='mock')
        result = adapter.synthesize('hello')
        self.assertEqual(result['provider'], 'mock')
        self.assertEqual(result['text'], 'hello')

    def test_invalid_text_rejected(self):
        adapter = TtsAdapter(provider='mock')
        with self.assertRaises(TtsError) as err:
            adapter.synthesize('  ')
        self.assertEqual(err.exception.code, 'ERR_TTS_INVALID_TEXT')

    def test_unknown_provider_rejected(self):
        adapter = TtsAdapter(provider='unknown')
        with self.assertRaises(TtsError) as err:
            adapter.synthesize('hello')
        self.assertEqual(err.exception.code, 'ERR_TTS_PROVIDER_UNKNOWN')


if __name__ == '__main__':
    unittest.main()
