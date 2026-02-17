# Deskling

![Status](https://img.shields.io/badge/status-MVP%20demo-0a7ea4)
![Roadmap](https://img.shields.io/badge/roadmap-character--first-1f6feb)
![Specs](https://img.shields.io/badge/specs-MVP%20focused-2ea043)
![Stack](https://img.shields.io/badge/stack-Electron-f59e0b)
![Privacy](https://img.shields.io/badge/privacy-local--first-8b5cf6)

Desktop character companion with a draggable sprite, speech bubbles, and delightful interactions.

## Project Status
This repository is in **MVP demo development** focusing on visual character experience.
Full voice assistant features are preserved in the codebase but not in active development focus.

## Start Here
- **MVP scope** (current focus): [`specs/mvp_scope.md`](specs/mvp_scope.md)
- Roadmap (source of truth for sequencing): [`ROADMAP.md`](ROADMAP.md)
- Product specs index: [`specs/README.md`](specs/README.md)
- Full product vision (post-MVP): [`specs/project_scope.md`](specs/project_scope.md)

## Vision (MVP)
Deskling is a delightful desktop character that:
- floats on your screen as a draggable sprite
- displays speech bubbles with messages
- has smooth animations and minimal interactions
- runs as a lightweight Electron app

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
Current repository includes MVP character demo UI and preserved backend services.

**MVP development commands** (desktop character):
```bash
cd apps/desktop-ui
npm install
npm run character        # Launch character demo
npm run character:dev    # Launch with developer tools
```

**Full product commands** (multi-service mode - preserved):
```bash
npm run dev     # Start all services via orchestration script
npm run build   # Build all components
```

## Quick Start (MVP Demo)

1. Clone the repository
2. Navigate to the desktop UI: `cd apps/desktop-ui`
3. Install dependencies: `npm install`
4. Run the character demo: `npm run character`
5. Interact with your new desktop buddy!
   - Drag the window to move the character
   - Click the character to see messages
   - Watch the idle animations

See [`apps/desktop-ui/README-CHARACTER.md`](apps/desktop-ui/README-CHARACTER.md) for more details.

## Contributing
1. Read [`ROADMAP.md`](ROADMAP.md) first.
2. Pick or define the target task ID.
3. Check/update related spec files under `specs/`.
4. Implement in small, focused commits.

## Documentation Map
- Contributor/agent operating conventions: [`AGENTS.md`](AGENTS.md)
- Product specs index: [`specs/README.md`](specs/README.md)
- Project roadmap: [`ROADMAP.md`](ROADMAP.md)
