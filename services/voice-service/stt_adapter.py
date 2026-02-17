"""STT adapter abstraction for voice-service."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SttError(Exception):
    code: str
    message: str


class SttAdapter:
    def __init__(self, provider: str = 'mock') -> None:
        self.provider = provider

    def transcribe_chunks(self, chunks: list[str]) -> str:
        if self.provider == 'mock':
            return ' '.join(chunk.strip() for chunk in chunks if isinstance(chunk, str) and chunk.strip()).strip()

        if self.provider == 'faster-whisper':
            try:
                import faster_whisper  # noqa: F401
            except ImportError as err:
                raise SttError('ERR_STT_PROVIDER_MISSING', f'faster-whisper is not installed: {err}') from err

            raise SttError('ERR_STT_NOT_IMPLEMENTED', 'audio-file transcription path not implemented in v0 baseline')

        raise SttError('ERR_STT_PROVIDER_UNKNOWN', f'unknown stt provider: {self.provider}')
