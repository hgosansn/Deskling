import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'voice-service'))

from capture import PushToTalkSession  # noqa: E402


class PushToTalkTests(unittest.TestCase):
    def test_start_and_stop_emit_events(self):
        events = []
        session = PushToTalkSession(events.append)

        trace_id = session.start_capture()
        session.add_transcript_chunk('hello')
        session.add_transcript_chunk('deskling')
        final_event = session.stop_capture()

        self.assertEqual(events[0].topic, 'voice.capture.start')
        self.assertEqual(events[0].trace_id, trace_id)
        self.assertEqual(final_event.topic, 'voice.stt.final')
        self.assertEqual(final_event.payload['text'], 'hello deskling')

    def test_stop_without_start(self):
        events = []
        session = PushToTalkSession(events.append)
        self.assertIsNone(session.stop_capture())
        self.assertEqual(len(events), 0)

    def test_custom_finalize_callback_used(self):
        events = []
        session = PushToTalkSession(events.append, finalize_transcript=lambda chunks: '|'.join(chunks))
        session.start_capture()
        session.add_transcript_chunk('a')
        session.add_transcript_chunk('b')
        final_event = session.stop_capture()
        self.assertEqual(final_event.payload['text'], 'a|b')


if __name__ == '__main__':
    unittest.main()
