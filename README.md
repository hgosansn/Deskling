# Deskling

![Status](https://img.shields.io/badge/status-Rust%20MVP-ff7a00)
![Roadmap](https://img.shields.io/badge/roadmap-character--first-1f6feb)
![Language](https://img.shields.io/badge/language-Rust-ff7a00)
![Stack](https://img.shields.io/badge/framework-egui-2ea043)
![Privacy](https://img.shields.io/badge/privacy-local--first-8b5cf6)

Desktop character companion built with Rust using egui/eframe - native performance, minimal footprint.

## 🦀 Rust Implementation (Current)

The project has been reimplemented in Rust for superior performance and native desktop integration.

**Quick Start:**
```bash
cd deskling-character
cargo build --release
cargo run --release
```

### Why Rust?

| Metric | Rust (egui) | Electron (Previous) |
|--------|-------------|---------------------|
| Startup Time | <0.5s | ~2-3s |
| Memory Usage | ~30 MB | ~150 MB |
| Binary Size | 9.2 MB | 100+ MB |
| CPU Usage | Minimal | Higher |
| Native Feel | ✅ Yes | ❌ No |

## Project Status
**Current focus**: Rust-based MVP character demo with native performance.
The codebase has transitioned to Rust-only for the desktop character application.

## Start Here
- **Rust Implementation** (current): [`deskling-character/README.md`](deskling-character/README.md)
- **MVP scope**: [`specs/mvp_scope.md`](specs/mvp_scope.md)
- Roadmap (source of truth for sequencing): [`ROADMAP.md`](ROADMAP.md)
- Product specs index: [`specs/README.md`](specs/README.md)

## Vision (Rust MVP)
Deskling is a native desktop character that:
- floats on your screen as a draggable sprite
- displays speech bubbles with messages
- has smooth 60 FPS animations with minimal CPU usage
- runs as a lightweight Rust/egui application
- provides instant startup and native OS integration

### Features
1. **Transparent, frameless window** - Always-on-top overlay
2. **Animated stickman character** - Custom SVG-style rendering with egui painter
3. **Speech bubble system** - Click for 10 different messages
4. **Smooth animations** - Idle bounce, talking bob, hover zoom
5. **Draggable interface** - Move character anywhere on screen
6. **Native performance** - Compiled Rust with minimal overhead

## Vision (Full Product - Post-MVP)
The full vision includes a local-first assistant that can:
- accept typed and push-to-talk voice input
- propose clear plans for risky actions
- execute approved desktop/web tools through policy controls
- respond with text and speech
- swap character skins without runtime restarts

*Note: Full assistant features are implemented but not part of MVP demo focus.*

## Principles (MVP)
- Visual delight and smooth interactions first
- Minimal dependencies for demo simplicity
- Cross-platform compatibility (Fedora primary)

## Principles (Full Product)
- Local-first by default
- Explicit confirmation for medium/high risk actions
- Modular services connected through a single IPC hub
- Auditability for all tool actions

## Architecture Snapshot (Full Product - Preserved)
The full product architecture includes multiple services:
- `desktop-ui` (Electron): overlay, chat bubble, confirmations
- `ipc-hub` (Python): local WebSocket bus, auth, routing, heartbeat
- `agent-core` (Python): plan generation, tool proposals, response composition
- `automation-service` (Python): policy-enforced tool execution + audit logs
- `voice-service` (Python): STT/TTS and interruption handling
- `skin-service` (optional): skin management and generation hooks

**For MVP demo**: Only the desktop-ui is actively used in standalone mode.

See full details in [`specs/architecture.md`](specs/architecture.md).

## Roadmap Reference
All implementation work must map to a roadmap task ID (`P#-T#`) before coding starts.
If scope changes, update both [`ROADMAP.md`](ROADMAP.md) and impacted spec files in `specs/` in the same session.

## Development Notes
Current repository features Rust-based character demo with native performance.

**Rust MVP commands** (desktop character):
```bash
cd deskling-character
cargo build --release       # Build optimized binary
cargo run --release         # Run the character demo
./demo.sh                   # Show info about the demo
```

**Binary info:**
- Location: `deskling-character/target/release/deskling-character`
- Size: ~9.2 MB (stripped and optimized)
- Dependencies: egui 0.31, eframe 0.31

**System requirements:**
- Rust toolchain (1.70+)
- Linux: libxcb, libxkbcommon, wayland development packages
- See `deskling-character/README.md` for platform-specific dependencies

## Quick Start (Rust MVP)

1. Clone the repository
2. Install Rust toolchain: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
3. Navigate to Rust app: `cd deskling-character`
4. Build and run: `cargo run --release`
5. Interact with your desktop buddy!
   - Drag the window to move the character
   - Click the character to see messages
   - Watch the smooth 60 FPS animations

See [`deskling-character/README.md`](deskling-character/README.md) for detailed documentation.

### Previous Implementation (Preserved)
The original Electron implementation is preserved in `apps/desktop-ui/` for reference.
The Rust version provides significantly better performance and native integration.

## Contributing
1. Read [`ROADMAP.md`](ROADMAP.md) first.
2. Pick or define the target task ID.
3. Check/update related spec files under `specs/`.
4. Implement in small, focused commits.

## Documentation Map
- Contributor/agent operating conventions: [`AGENTS.md`](AGENTS.md)
- Product specs index: [`specs/README.md`](specs/README.md)
- Project roadmap: [`ROADMAP.md`](ROADMAP.md)
