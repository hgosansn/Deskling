# Deskling

![Status](https://img.shields.io/badge/status-active%20planning-0a7ea4)
![Roadmap](https://img.shields.io/badge/roadmap-authoritative-1f6feb)
![Specs](https://img.shields.io/badge/specs-required-2ea043)
![Stack](https://img.shields.io/badge/stack-Tauri%20%2B%20Python-f59e0b)
![Privacy](https://img.shields.io/badge/privacy-local--first-8b5cf6)

Cross-platform desktop voice assistant with a floating character UI, local-first voice pipeline, safe tool execution, and a skin-based appearance system.

## Project Status
This repository is in active build planning and foundational implementation.
Execution order, scope, and priorities are managed in the roadmap.

## Start Here
- Roadmap (source of truth for sequencing): [`ROADMAP.md`](ROADMAP.md)
- Product/context specs index: [`specs/README.md`](specs/README.md)
- Scope definition: [`specs/project_scope.md`](specs/project_scope.md)
- Architecture baseline: [`specs/architecture.md`](specs/architecture.md)
- IPC contract: [`specs/ipc_protocol.md`](specs/ipc_protocol.md)
- Tool safety model: [`specs/tool_system.md`](specs/tool_system.md)

## Vision
TaskSprite is a local-first assistant that can:
- accept typed and push-to-talk voice input
- propose clear plans for risky actions
- execute approved desktop/web tools through policy controls
- respond with text and speech
- swap character skins without runtime restarts

## Principles
- Local-first by default
- Explicit confirmation for medium/high risk actions
- Modular services connected through a single IPC hub
- Auditability for all tool actions

## Architecture Snapshot
High-level components:
- `desktop-ui` (Tauri): overlay, chat bubble, confirmations
- `ipc-hub` (Python): local WebSocket bus, auth, routing, heartbeat
- `agent-core` (Python): plan generation, tool proposals, response composition
- `automation-service` (Python): policy-enforced tool execution + audit logs
- `voice-service` (Python): STT/TTS and interruption handling
- `skin-service` (optional): skin management and generation hooks

See full details in [`specs/architecture.md`](specs/architecture.md).

## Roadmap Reference
All implementation work must map to a roadmap task ID (`P#-T#`) before coding starts.
If scope changes, update both [`ROADMAP.md`](ROADMAP.md) and impacted spec files in `specs/` in the same session.

## Development Notes
Monorepo scaffold is now Tauri-first for desktop UI and Python-first for services.

Common commands:
- `npm run dev` (frontend shell in `apps/desktop-ui`)
- `npm run tauri:dev` (desktop app)
- `npm run build` (frontend build)
- `./verify.sh` (frontend build + Rust host check)
- `./scripts/dev-up.sh` (start `ipc-hub` + `agent-core` + desktop-ui dev shell)
- `python3 scripts/typed_chat_smoke.py` (typed-chat IPC smoke test)

## Contributing
1. Read [`ROADMAP.md`](ROADMAP.md) first.
2. Pick or define the target task ID.
3. Check/update related spec files under `specs/`.
4. Implement in small, focused commits.

## Documentation Map
- Contributor/agent operating conventions: [`AGENTS.md`](AGENTS.md)
- Product specs index: [`specs/README.md`](specs/README.md)
- Project roadmap: [`ROADMAP.md`](ROADMAP.md)
