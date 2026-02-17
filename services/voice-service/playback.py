"""Playback controller with barge-in interruption support."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from capture import VoiceEvent


@dataclass
class PlaybackState:
    speaking: bool
    trace_id: str


class PlaybackController:
    def __init__(self, emit: Callable[[VoiceEvent], None]):
        self._emit = emit
        self._state = PlaybackState(speaking=False, trace_id='')

    @property
    def speaking(self) -> bool:
        return self._state.speaking

    def start(self, trace_id: str, text: str) -> None:
        self._state = PlaybackState(speaking=True, trace_id=trace_id)
        self._emit(VoiceEvent(topic='voice.tts.playback_start', trace_id=trace_id, payload={'text': text}))

    def interrupt(self, trace_id: str, reason: str = 'barge_in') -> bool:
        if not self._state.speaking:
            return False

        current = self._state.trace_id
        self._state = PlaybackState(speaking=False, trace_id='')
        self._emit(VoiceEvent(topic='voice.tts.cancel', trace_id=trace_id or current, payload={'reason': reason}))
        return True

    def complete(self, trace_id: str) -> None:
        if self._state.speaking:
            self._state = PlaybackState(speaking=False, trace_id='')
            self._emit(VoiceEvent(topic='voice.tts.playback_done', trace_id=trace_id, payload={}))
