"""Push-to-talk capture primitives for voice-service v0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from uuid import uuid4


@dataclass
class VoiceEvent:
    topic: str
    trace_id: str
    payload: dict


class PushToTalkSession:
    def __init__(self, emit: Callable[[VoiceEvent], None], finalize_transcript: Callable[[list[str]], str] | None = None):
        self._emit = emit
        self._finalize_transcript = finalize_transcript or self._default_finalize_transcript
        self._active = False
        self._trace_id = ''
        self._chunks: list[str] = []

    def start_capture(self) -> str:
        if self._active:
            return self._trace_id

        self._active = True
        self._trace_id = uuid4().hex
        self._chunks = []
        self._emit(VoiceEvent(topic='voice.capture.start', trace_id=self._trace_id, payload={'mode': 'push_to_talk'}))
        return self._trace_id

    def add_transcript_chunk(self, text: str) -> None:
        if not self._active:
            return
        if isinstance(text, str) and text.strip():
            self._chunks.append(text.strip())

    def stop_capture(self) -> VoiceEvent | None:
        if not self._active:
            return None

        final_text = self._finalize_transcript(self._chunks)
        self._active = False

        event = VoiceEvent(
            topic='voice.stt.final',
            trace_id=self._trace_id,
            payload={'text': final_text}
        )
        self._emit(event)
        return event

    @staticmethod
    def _default_finalize_transcript(chunks: list[str]) -> str:
        return ' '.join(chunks).strip()
