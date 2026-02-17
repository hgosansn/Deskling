#!/usr/bin/env python3
"""Voice-service baseline with push-to-talk capture event flow."""

from __future__ import annotations

import logging
import time

from capture import PushToTalkSession, VoiceEvent
from playback import PlaybackController
from stt_adapter import SttAdapter
from tts_adapter import TtsAdapter
from tasksprite_common import get_service_logger, new_trace_id


def main() -> None:
    logger = get_service_logger('voice-service')
    logger.event(logging.INFO, 'service.start', new_trace_id(), mode='push-to-talk-v0')
    stt = SttAdapter(provider='mock')
    tts = TtsAdapter(provider='mock')

    def emit(event: VoiceEvent) -> None:
        logger.event(logging.INFO, event.topic, event.trace_id, **event.payload)

    session = PushToTalkSession(emit, finalize_transcript=stt.transcribe_chunks)
    playback = PlaybackController(emit)

    try:
        while True:
            trace = session.start_capture()
            session.add_transcript_chunk('voice')
            session.add_transcript_chunk('service')
            final_event = session.stop_capture()
            if final_event and final_event.payload.get('text'):
                tts_result = tts.synthesize(final_event.payload['text'])
                logger.event(logging.INFO, 'voice.tts.speak', trace, **tts_result)
                playback.start(trace, tts_result['text'])
                playback.interrupt(trace, reason='barge_in')
            logger.event(logging.INFO, 'audio.idle', trace, capture='off', playback='off')
            time.sleep(5)
    except KeyboardInterrupt:
        logger.event(logging.INFO, 'service.stop', new_trace_id(), reason='interrupt')


if __name__ == '__main__':
    main()
