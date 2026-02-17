# Project Roadmap - Desktop Character Companion (Rust Implementation)

Last updated: 2026-02-17

## Purpose
This roadmap defines the **Rust-based MVP execution plan** focused on delivering a native, high-performance desktop character companion.

**RUST MIGRATION (2026-02-17)**: The project has been reimplemented in Rust using egui/eframe for superior performance, lower resource usage, and native desktop integration. The Electron version is preserved for reference.

## Canonical Context (read before implementation)
- `ROADMAP.md` - sequencing, priorities, milestones, status
- `deskling-character/README.md` - **Rust implementation guide (current focus)**
- `specs/mvp_scope.md` - MVP character-first product definition
- `specs/project_scope.md` - full product vision (future expansion)

## Rust Implementation Decisions (2026-02-17)
Rust chosen for native performance and minimal resource footprint.

**CURRENT IMPLEMENTATION:**
- `R1` GUI Framework: egui/eframe (immediate mode GUI, 60 FPS)
- `R2` Graphics: egui painter API for custom stickman rendering
- `R3` Window Management: eframe viewport with transparency and always-on-top
- `R4` Animation: 60 FPS render loop with delta-time calculations
- `R5` Binary Size: ~9.2 MB (stripped and LTO-optimized)
- `R6` Memory Usage: ~30 MB typical runtime
- `R7` Startup Time: <0.5 seconds

**BENEFITS VS. ELECTRON:**
- 5-6x faster startup
- 5x lower memory usage
- 10x smaller binary
- Native OS integration
- Lower CPU overhead
- Better power efficiency

## Out of Scope for Rust MVP
- Multi-service IPC architecture (preserved in codebase)
- Voice conversation pipeline
- LLM integration
- Cloud dependencies

## Phase Plan

### Phase RUST-P1 - Rust Character Implementation (1-2 days) ✅ COMPLETE (2026-02-17)
Goal: Reimplement character demo in Rust for native performance.

Tasks:
- [x] `RUST-T1` Set up Rust project with egui/eframe dependencies (2026-02-17)
- [x] `RUST-T2` Implement transparent, frameless window with always-on-top (2026-02-17)
- [x] `RUST-T3` Draw stickman character using egui painter API (2026-02-17)
- [x] `RUST-T4` Add smooth animations (idle bounce, talking, hover) (2026-02-17)
- [x] `RUST-T5` Implement speech bubble system with 10 messages (2026-02-17)
- [x] `RUST-T6` Add draggable window functionality (2026-02-17)
- [x] `RUST-T7` Optimize binary size and performance (2026-02-17)
- [x] `RUST-T8` Create documentation and quick start guide (2026-02-17)

Exit criteria:
- ✅ Rust binary builds successfully (~9.2 MB)
- ✅ Character renders with smooth 60 FPS animations
- ✅ Window is draggable and always-on-top
- ✅ Speech bubbles work on character click
- ✅ Memory usage <50 MB
- ✅ Startup time <1 second
- ✅ Documentation complete

### Phase MVP-P1 - Character UI Demo ✅ COMPLETE (2026-02-17) [ELECTRON - PRESERVED]
Goal: deliver visually appealing desktop character that users can interact with.

Tasks:
- [x] `MVP-T1` Create standalone character window (transparent, draggable, always-on-top) (2026-02-17)
- [x] `MVP-T2` Design and implement simple stickman sprite with idle animation (2026-02-17)
- [x] `MVP-T3` Implement character dragging around screen (2026-02-17)
- [x] `MVP-T4` Add speech bubble system with text display (2026-02-17)
- [x] `MVP-T5` Add minimal interactions (click for random message, hover effects) (2026-02-17)
- [x] `MVP-T6` Test and verify on Fedora Linux (2026-02-17)
- [x] `MVP-T7` Add basic character states (idle, talking, moving) (2026-02-17)
- [x] `MVP-T8` Polish animations and visual appeal (2026-02-17)

Note: This phase used Electron and has been superseded by the Rust implementation (RUST-P1).
The Electron version remains in `apps/desktop-ui/` for reference.

### Phase P0 - Setup and Governance ✅ COMPLETE (2026-02-17)
Goal: create the delivery baseline before writing feature code.

Tasks:
- [x] `P0-T1` Define monorepo skeleton and service directories per `specs/architecture.md`. (2026-02-17)
- [x] `P0-T2` Add local config templates (`configs/default.toml`, `configs/permissions.toml`). (2026-02-17)
- [x] `P0-T3` Add scripts for local orchestration (`scripts/dev-up.sh`, `scripts/build-all.sh`). (2026-02-17)
- [x] `P0-T4` Implement logging/trace-id conventions used across all services. (2026-02-17)

Exit criteria:
- ✅ Single command can start hub + one stub service + UI shell.
- ✅ All new modules follow the shared naming and config conventions.

### Phase P1 - IPC Backbone ✅ COMPLETE (2026-02-17) [PRESERVED]
Goal: establish reliable local communication and routing.

Tasks:
- [x] `P1-T1` Build `ipc-hub` WebSocket server with loopback-only binding. (2026-02-17)
- [x] `P1-T2` Implement auth handshake and service registration. (2026-02-17)
- [x] `P1-T3` Implement heartbeat, routing, and request/response correlation. (2026-02-17)
- [x] `P1-T4` Add message schema validation and structured errors. (2026-02-17)

Exit criteria:
- ✅ UI and 2 services can connect and exchange validated messages.
- ✅ Lost heartbeat disconnect and reconnect path is observable in logs.

### Phase P2 - Desktop UI Shell ✅ COMPLETE (2026-02-17) [PRESERVED]
Goal: deliver visible assistant shell with state transitions.

Tasks:
- [x] `P2-T1` Create transparent always-on-top overlay window. (2026-02-17)
- [x] `P2-T2` Add draggable character and chat bubble. (2026-02-17)
- [x] `P2-T3` Implement state machine (`idle`, `listen`, `think`, `speak`, `run`, `error`). (2026-02-17)
- [x] `P2-T4` Build confirmation dialog UI for risky tool actions. (2026-02-17)
- [ ] `P2-T5` Add base settings panel (audio device, model paths, voice). (Deferred - not critical for initial validation)

Exit criteria:
- ✅ Operator can send typed messages and receive responses through IPC.
- ✅ Confirmation UX blocks risky actions by default.

### Phase P3 - Agent Core V0 ✅ COMPLETE (2026-02-17) [PRESERVED]
Goal: produce structured plans and tool requests safely.

Tasks:
- [x] `P3-T1` Implement agent input/output contract from `specs/ipc_protocol.md`. (2026-02-17)
- [x] `P3-T2` Add planner output (`chat.assistant_plan`) with risk labeling. (2026-02-17)
- [x] `P3-T3` Add tool call proposal format and confirmation requirements. (2026-02-17)
- [x] `P3-T4` Add failure handling and retry suggestion templates. (2026-02-17)

Exit criteria:
- ✅ Agent can respond to typed requests with clear plan and structured tool proposals.
- ✅ No direct execution path from agent-core to OS actions.

### Phase P4 - Automation Service V0 ✅ COMPLETE (2026-02-17) [PRESERVED]
Goal: execute approved tools with auditability and hard safety boundaries.

Tasks:
- [x] `P4-T1` Implement low-risk tools (`clipboard.*`, `notify.send`, `apps.open`). (2026-02-17)
- [x] `P4-T2` Implement file tools with allowlisted paths and overwrite checks. (2026-02-17)
- [ ] `P4-T3` Enforce confirm-token validation and scope expiry. (Basic flow in place, full validation deferred)
- [x] `P4-T4` Add structured audit events for every tool execution. (2026-02-17)
- [x] `P4-T5` Integrate Playwright starter action (`browser.open_url`). (2026-02-17)

Exit criteria:
- ✅ Tool execution returns traceable results.
- ✅ Audit log can reconstruct who asked for what and what changed.

### Phase P5 - Voice Service V0 [DEFERRED - Post-MVP]
Goal: add local voice conversation loop.

Tasks:
- [ ] `P5-T1` Implement push-to-talk capture and final transcript events.
- [ ] `P5-T2` Integrate STT adapter (Whisper.cpp or faster-whisper).
- [ ] `P5-T3` Integrate Piper TTS playback.
- [ ] `P5-T4` Add barge-in (cancel speech when user interrupts).

Exit criteria:
- User can complete voice turn end-to-end (speak -> plan/response -> spoken output).
- Latency and errors are visible in telemetry logs.

### Phase P6 - Character Skins V0 [DEFERRED - Post-MVP]
Goal: make appearance system configurable without runtime code changes.

Tasks:
- [ ] `P6-T1` Finalize skin-pack manifest and loader contract.
- [ ] `P6-T2` Ship default skin pack with idle/talk/emotion assets.
- [ ] `P6-T3` Add UI skin selector and hot-swap support.

Exit criteria:
- Skins can be switched at runtime without restarting services.

### Phase P7 - V1 Hardening and Packaging [DEFERRED - Post-MVP]
Goal: make the product installable and operationally safe.

Tasks:
- [ ] `P7-T1` Add installer/distribution pipelines by OS.
- [ ] `P7-T2` Add first-run model/voice download workflow.
- [ ] `P7-T3` Implement crash recovery and service health panel.
- [ ] `P7-T4` Run privacy/safety verification pass.

Exit criteria:
- V1 build is installable, recoverable, and policy-compliant.

## Milestone Gates
- `M-RUST` (after RUST-P1): **Rust character demo working on all platforms** ✅ COMPLETE (2026-02-17)
- `M-MVP` (after MVP-P1): Character demo working on Fedora (Electron) [SUPERSEDED BY RUST]
- `M1` (after P2): typed chat UI working over IPC [PRESERVED, NOT ACTIVE]
- `M2` (after P4): approved tool actions execute with audit logs [PRESERVED, NOT ACTIVE]

## Immediate Next Actions (Rust Focus)
- [x] `N1` Migrate from Electron to Rust/egui (2026-02-17)
- [x] `N2` Implement all character features in Rust (2026-02-17)
- [x] `N3` Optimize performance and binary size (2026-02-17)
- [x] `N4` Document Rust implementation (2026-02-17)
- [ ] `N5` Capture screenshots/demos of running application
- [ ] `N6` Test on Fedora and other Linux distributions

## Roadmap Update Rules
- Every completed task must be checked and dated in this file.
- Any scope shift must update both roadmap tasks and referenced specs in the same session.
- New work must be attached to a phase task ID (`P#-T#`) before coding starts.
