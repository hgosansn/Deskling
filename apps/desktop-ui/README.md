# Desktop UI

Electron-based overlay interface for the voice assistant.

## Responsibilities
- Transparent always-on-top overlay window
- User input capture (typed + push-to-talk)
- Display of plan/confirmation flow
- State transitions visualization (idle, listen, think, speak, run, error)

## Tech Stack
- Electron
- React/Preact (reusing existing)
- WebSocket client for IPC

## Related Specs
- `specs/architecture.md`
- `specs/project_scope.md`

## Related Roadmap
- P2-T1: Create transparent always-on-top overlay window
- P2-T2: Add draggable character and chat bubble
- P2-T3: Implement state machine
- P2-T4: Build confirmation dialog UI
- P2-T5: Add base settings panel
