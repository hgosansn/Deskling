import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'agent-core'))

from failure_templates import failure_message  # noqa: E402


class FailureTemplateTests(unittest.TestCase):
    def test_known_error_has_retry_guidance(self):
        text = failure_message('ERR_EMPTY_TEXT')
        self.assertIn('Retry:', text)

    def test_unknown_error_has_fallback(self):
        text = failure_message('ERR_UNKNOWN', 'raw detail')
        self.assertIn('rephrase', text.lower())
        self.assertIn('raw detail', text)


if __name__ == '__main__':
    unittest.main()
