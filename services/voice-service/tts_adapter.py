"""TTS adapter abstraction for voice-service."""

from __future__ import annotations

from dataclasses import dataclass
import shutil


@dataclass
class TtsError(Exception):
    code: str
    message: str


class TtsAdapter:
    def __init__(self, provider: str = 'mock') -> None:
        self.provider = provider

    def synthesize(self, text: str, voice: str = 'piper:en_US-amy-medium') -> dict:
        if not isinstance(text, str) or not text.strip():
            raise TtsError('ERR_TTS_INVALID_TEXT', 'tts requires non-empty text')

        if self.provider == 'mock':
            return {
                'provider': 'mock',
                'voice': voice,
                'text': text.strip(),
                'audio_ref': 'memory://mock-audio'
            }

        if self.provider == 'piper':
            if shutil.which('piper') is None:
                raise TtsError('ERR_TTS_PROVIDER_MISSING', 'piper executable not found')
            return {
                'provider': 'piper',
                'voice': voice,
                'text': text.strip(),
                'audio_ref': 'file://piper-output.wav'
            }

        raise TtsError('ERR_TTS_PROVIDER_UNKNOWN', f'unknown tts provider: {self.provider}')
