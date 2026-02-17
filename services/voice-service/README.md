# Voice Service

Speech-to-text and text-to-speech pipeline.

## Responsibilities
- Microphone capture and transcript generation
- TTS generation and playback controls
- Barge-in interruption handling

## Tech Stack
- Python 3.10+
- Whisper.cpp or faster-whisper for STT
- Piper for TTS
- WebSocket client for IPC

## Related Specs
- `specs/architecture.md`
- `specs/ipc_protocol.md`

## Related Roadmap
- P5-T1: Implement push-to-talk capture and final transcript events
- P5-T2: Integrate STT adapter
- P5-T3: Integrate Piper TTS playback
- P5-T4: Add barge-in (cancel speech when user interrupts)
