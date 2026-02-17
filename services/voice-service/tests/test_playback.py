import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'voice-service'))

from playback import PlaybackController  # noqa: E402


class PlaybackControllerTests(unittest.TestCase):
    def test_start_and_complete(self):
        events = []
        ctrl = PlaybackController(events.append)

        ctrl.start('trace-1', 'hello')
        self.assertTrue(ctrl.speaking)
        ctrl.complete('trace-1')
        self.assertFalse(ctrl.speaking)
        topics = [event.topic for event in events]
        self.assertEqual(topics, ['voice.tts.playback_start', 'voice.tts.playback_done'])

    def test_interrupt_emits_cancel(self):
        events = []
        ctrl = PlaybackController(events.append)

        ctrl.start('trace-2', 'hello')
        interrupted = ctrl.interrupt('trace-2')

        self.assertTrue(interrupted)
        self.assertFalse(ctrl.speaking)
        self.assertEqual(events[-1].topic, 'voice.tts.cancel')


if __name__ == '__main__':
    unittest.main()
