# Deskling

![Status](https://img.shields.io/badge/status-dual%20implementation-0a7ea4)
![Roadmap](https://img.shields.io/badge/roadmap-authoritative-1f6feb)
![Specs](https://img.shields.io/badge/specs-required-2ea043)
![Stack](https://img.shields.io/badge/stack-Rust%20%2B%20Tauri%20%2B%20Python-f59e0b)
![Privacy](https://img.shields.io/badge/privacy-local--first-8b5cf6)

Cross-platform desktop companion with two implementation paths:
1. **Rust Standalone** (🦀 MVP) - Lightweight character demo with egui/eframe
2. **Tauri + Python** (🎯 Full) - Complete voice assistant with multi-service architecture

## Project Status
This repository contains **two parallel implementations**:
- **Rust MVP**: Lightweight standalone character (`deskling-character/`)
- **Full Product**: Multi-service voice assistant architecture (Tauri + Python services)

Both implementations coexist to support different use cases and development approaches.

## Quick Start

### Option 1: Rust Standalone Character (MVP) 🦀
Lightweight desktop character with minimal dependencies:

```bash
cd deskling-character
cargo build --release
cargo run --release
```

**Features:**
- Transparent, frameless, always-on-top window
- Animated stickman character
- Speech bubbles (10 messages)
- Draggable window
- ~9 MB binary, <0.5s startup, ~30 MB RAM

**See:** [`deskling-character/README.md`](deskling-character/README.md)

### Option 2: Full Voice Assistant (Tauri + Python) 🎯
Complete multi-service voice assistant:

```bash
# Install dependencies
npm run install:all

# Start all services
npm run dev
```

**Features:**
- Voice conversation (STT/TTS)
- LLM-powered planning
- Tool execution with safety
- IPC-based multi-service architecture

## Start Here

### Rust Implementation (MVP)
- **Quick guide**: [`deskling-character/README.md`](deskling-character/README.md)
- **Visual reference**: [`docs/VISUAL_REFERENCE.md`](docs/VISUAL_REFERENCE.md)
- **Implementation notes**: [`RUST_IMPLEMENTATION.md`](RUST_IMPLEMENTATION.md)

### Full Product (Tauri + Python)
- Roadmap (source of truth for sequencing): [`ROADMAP.md`](ROADMAP.md)
- Product/context specs index: [`specs/README.md`](specs/README.md)
- Scope definition: [`specs/project_scope.md`](specs/project_scope.md)
- Architecture baseline: [`specs/architecture.md`](specs/architecture.md)
- IPC contract: [`specs/ipc_protocol.md`](specs/ipc_protocol.md)
- Tool safety model: [`specs/tool_system.md`](specs/tool_system.md)

## Vision

### Rust MVP Vision
Lightweight desktop character companion that:
- floats on your screen as a draggable sprite
- displays speech bubbles with messages
- has smooth 60 FPS animations
- runs as a ~9 MB Rust binary
- provides instant startup and minimal resource usage

### Full Product Vision
Complete local-first voice assistant that can:
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

## Architecture

### Rust Standalone (Current MVP)
Single-process Rust application using egui/eframe:
- Direct rendering with egui painter API
- Native window management
- No inter-process communication
- Minimal dependencies

### Full Product Architecture (Multi-Service)
High-level components:
- `desktop-ui` (Tauri): overlay, chat bubble, confirmations
- `deskling-character` (Rust): Standalone character alternative
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

### Rust MVP Development
```bash
cd deskling-character
cargo build --release    # Build optimized binary
cargo run --release      # Run character demo
./verify.sh             # Verify implementation
```

Binary location: `deskling-character/target/release/deskling-character` (~9.2 MB)

### Full Product Development (Tauri + Python)
Monorepo scaffold is Tauri-first for desktop UI and Python-first for services.

Common commands:
- `npm run dev` (frontend shell in `apps/desktop-ui`)
- `npm run tauri:dev` (desktop app)
- `npm run build` (frontend build)
- `./verify.sh` (frontend build + Rust host check)
- `./scripts/dev-up.sh` (start `ipc-hub` + `agent-core` + desktop-ui dev shell)
- `python3 scripts/typed_chat_smoke.py` (typed-chat IPC smoke test)

## Performance Comparison

| Metric | Rust MVP | Full Product |
|--------|----------|--------------|
| Startup Time | <0.5s | ~2-3s |
| Memory Usage | ~30 MB | Variable |
| Binary Size | 9.2 MB | Larger |
| Features | Character only | Full voice assistant |
| Dependencies | Minimal | Python + Node + Tauri |

## Contributing
1. Read [`ROADMAP.md`](ROADMAP.md) first.
2. Pick or define the target task ID.
3. Check/update related spec files under `specs/`.
4. Implement in small, focused commits.

## Documentation Map
- Contributor/agent operating conventions: [`AGENTS.md`](AGENTS.md)
- Product specs index: [`specs/README.md`](specs/README.md)
- Project roadmap: [`ROADMAP.md`](ROADMAP.md)
