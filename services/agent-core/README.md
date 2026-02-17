# Agent Core

Planning and model inference service.

## Responsibilities
- User intent handling and planning
- Model inference orchestration (Ollama-first)
- Tool proposal generation (not execution)
- Response composition and fallback behavior

## Tech Stack
- Python 3.10+
- Ollama client
- WebSocket client for IPC

## Related Specs
- `specs/architecture.md`
- `specs/ipc_protocol.md`
- `specs/tool_system.md`

## Related Roadmap
- P3-T1: Implement agent input/output contract
- P3-T2: Add planner output with risk labeling
- P3-T3: Add tool call proposal format
- P3-T4: Add failure handling and retry templates
