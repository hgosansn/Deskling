import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'voice-service'))

from stt_adapter import SttAdapter, SttError  # noqa: E402


class SttAdapterTests(unittest.TestCase):
    def test_mock_provider_transcribes_chunks(self):
        adapter = SttAdapter(provider='mock')
        text = adapter.transcribe_chunks(['hello', 'deskling'])
        self.assertEqual(text, 'hello deskling')

    def test_unknown_provider_rejected(self):
        adapter = SttAdapter(provider='unknown')
        with self.assertRaises(SttError) as err:
            adapter.transcribe_chunks(['x'])
        self.assertEqual(err.exception.code, 'ERR_STT_PROVIDER_UNKNOWN')


if __name__ == '__main__':
    unittest.main()
