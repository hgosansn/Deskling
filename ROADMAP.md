# Project Roadmap - Desktop Character Companion (MVP Rescope)

Last updated: 2026-02-17

## Purpose
This roadmap defines the **MVP-first execution plan** focused on delivering a delightful, visually appealing desktop character companion.

**MVP RESCOPE (2026-02-17)**: The primary goal is to create a working desktop demo with a draggable character sprite and speech bubbles. Full voice assistant features are retained in the codebase but deferred from active development focus.

## Canonical Context (read before implementation)
- `ROADMAP.md` - sequencing, priorities, milestones, status
- `specs/mvp_scope.md` - MVP character-first product definition
- `specs/project_scope.md` - full product vision (deferred features)
- `specs/architecture.md` - system architecture (preserved for future)
- `specs/ipc_protocol.md` - inter-process protocol (preserved for future)
- `specs/tool_system.md` - tool contracts (preserved for future)

## MVP Decisions (2026-02-17 Rescope)
Focus on delivering a delightful visual demo first, technical features second.

**MVP SCOPE (In Active Development):**
- `M1` Electron desktop UI with transparent, always-on-top window
- `M2` Simple animated stickman character sprite
- `M3` Draggable character around the screen
- `M4` Speech bubble system for text display
- `M5` Click/hover interactions with idle animations
- `M6` Works on Fedora Linux (and other platforms)

**PRESERVED (Implemented but Not MVP Focus):**
- `D1` Multi-process architecture (IPC hub, agent-core, services) - retained in codebase
- `D2` UI stack: Electron
- `D3-D12` Voice, LLM, tool execution features - preserved but not demo priority

## Out of Scope for MVP Demo
- Complex multi-service coordination
- Voice conversation pipeline
- LLM integration and tool execution
- Always-on wake-word
- Cloud dependencies

## Phase Plan

### Phase MVP-P1 - Character UI Demo (1-3 days) ✅ COMPLETE (2026-02-17)
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

Exit criteria:
- ✅ Character window launches and floats on screen
- ✅ User can drag character to any position
- ✅ Speech bubbles appear with sample text
- ✅ Works reliably on Fedora (and other OSes)
- ✅ Visually appealing and fun to interact with

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
- `M-MVP` (after MVP-P1): **Character demo working on Fedora** ✅ COMPLETE (2026-02-17)
- `M1` (after P2): typed chat UI working over IPC [COMPLETE, PRESERVED]
- `M2` (after P4): approved tool actions execute with audit logs [COMPLETE, PRESERVED]
- `M3` (after P5): local voice conversation stable [DEFERRED]
- `M4` (after P6): skin packs hot-swappable [DEFERRED]
- `M5` (after P7): packaged release candidate [DEFERRED]

## Immediate Next Actions (MVP Focus)
- [x] `N1` Update roadmap to reflect MVP character-first scope (2026-02-17)
- [x] `N2` Simplify desktop-ui to standalone character mode (2026-02-17)
- [x] `N3` Implement stickman sprite graphics (2026-02-17)
- [x] `N4` Add draggable character behavior (2026-02-17)
- [x] `N5` Create speech bubble system (2026-02-17)
- [x] `N6` Test on Fedora and capture demo screenshots (2026-02-17)

## Roadmap Update Rules
- Every completed task must be checked and dated in this file.
- Any scope shift must update both roadmap tasks and referenced specs in the same session.
- New work must be attached to a phase task ID (`P#-T#`) before coding starts.
