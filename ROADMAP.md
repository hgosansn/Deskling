# Project Roadmap - Cross-Platform Voice Desktop Mate

Last updated: 2026-02-16

## Purpose
This roadmap is the execution plan for building the product. It is intentionally concise and phase-driven.
Detailed design and implementation rules live in `specs/`.

## Canonical Context (read before implementation)
- `ROADMAP.md` - sequencing, priorities, milestones, status
- `specs/project_scope.md` - product definition, goals, non-goals, success criteria
- `specs/architecture.md` - system architecture, service boundaries, repository layout
- `specs/ipc_protocol.md` - inter-process protocol and conversation flows
- `specs/tool_system.md` - tool contracts, risk model, confirmation policy, initial tool set

## Pre-Start Decisions (Locked)
These are committed choices for v1 unless explicitly changed in roadmap updates.

- `D1` Runtime split: multi-process local system (`desktop-ui`, `ipc-hub`, `agent-core`, `voice-service`, `automation-service`, optional `skin-service`).
- `D2` UI stack: Electron for v1 velocity. Tauri is a post-v1 optimization path.
- `D3` Core service language: Python (fast AI iteration, mature local inference ecosystem).
- `D4` IPC transport: local WebSocket hub on loopback only (`127.0.0.1`), JSON envelopes, heartbeat, token auth.
- `D5` LLM runtime: Ollama-first abstraction with provider interface for future remote models.
- `D6` STT: Whisper.cpp / faster-whisper adapter (local-first, offline-capable).
- `D7` TTS: Piper local voices.
- `D8` Browser automation: Playwright as default web execution path.
- `D9` Desktop automation safety: confirmation-token gate for medium/high risk actions.
- `D10` Character system: skin-pack format for v1; live generation is v1.5+.
- `D11` Initial release mode: push-to-talk first; wake-word deferred.
- `D12` Data/privacy baseline: local-first storage, audit logs for tool actions, no secret leakage in assistant responses.

## Out of Scope for V1
- Always-on wake-word by default
- Fully autonomous destructive actions without confirmation
- Real-time generated 3D avatar creation
- Cloud dependency as required path

## Phase Plan

### Phase P0 - Setup and Governance (1-2 days) ✅ COMPLETE (2026-02-17)
Goal: create the delivery baseline before writing feature code.

Tasks:
- [x] `P0-T1` Define monorepo skeleton and service directories per `specs/architecture.md`. (2026-02-17)
- [x] `P0-T2` Add local config templates (`configs/default.toml`, `configs/permissions.toml`). (2026-02-17)
- [x] `P0-T3` Add scripts for local orchestration (`scripts/dev-up.sh`, `scripts/build-all.sh`). (2026-02-17)
- [x] `P0-T4` Implement logging/trace-id conventions used across all services. (2026-02-17)

Exit criteria:
- ✅ Single command can start hub + one stub service + UI shell.
- ✅ All new modules follow the shared naming and config conventions.

### Phase P1 - IPC Backbone (2-4 days) ✅ COMPLETE (2026-02-17)
Goal: establish reliable local communication and routing.

Tasks:
- [x] `P1-T1` Build `ipc-hub` WebSocket server with loopback-only binding. (2026-02-17)
- [x] `P1-T2` Implement auth handshake and service registration. (2026-02-17)
- [x] `P1-T3` Implement heartbeat, routing, and request/response correlation. (2026-02-17)
- [x] `P1-T4` Add message schema validation and structured errors. (2026-02-17)

Exit criteria:
- ✅ UI and 2 services can connect and exchange validated messages.
- ✅ Lost heartbeat disconnect and reconnect path is observable in logs.

### Phase P2 - Desktop UI Shell (3-6 days) ✅ COMPLETE (2026-02-17)
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

### Phase P3 - Agent Core V0 (3-7 days) ✅ COMPLETE (2026-02-17)
Goal: produce structured plans and tool requests safely.

Tasks:
- [x] `P3-T1` Implement agent input/output contract from `specs/ipc_protocol.md`. (2026-02-17)
- [x] `P3-T2` Add planner output (`chat.assistant_plan`) with risk labeling. (2026-02-17)
- [x] `P3-T3` Add tool call proposal format and confirmation requirements. (2026-02-17)
- [x] `P3-T4` Add failure handling and retry suggestion templates. (2026-02-17)

Exit criteria:
- ✅ Agent can respond to typed requests with clear plan and structured tool proposals.
- ✅ No direct execution path from agent-core to OS actions.

### Phase P4 - Automation Service V0 (4-10 days)
Goal: execute approved tools with auditability and hard safety boundaries.

Tasks:
- [ ] `P4-T1` Implement low-risk tools (`clipboard.*`, `notify.send`, `apps.open`).
- [ ] `P4-T2` Implement file tools with allowlisted paths and overwrite checks.
- [ ] `P4-T3` Enforce confirm-token validation and scope expiry.
- [ ] `P4-T4` Add structured audit events for every tool execution.
- [ ] `P4-T5` Integrate Playwright starter action (`browser.open_url`).

Exit criteria:
- Tool execution requires policy compliance and returns traceable results.
- Audit log can reconstruct who asked for what and what changed.

### Phase P5 - Voice Service V0 (4-10 days)
Goal: add local voice conversation loop.

Tasks:
- [ ] `P5-T1` Implement push-to-talk capture and final transcript events.
- [ ] `P5-T2` Integrate STT adapter (Whisper.cpp or faster-whisper).
- [ ] `P5-T3` Integrate Piper TTS playback.
- [ ] `P5-T4` Add barge-in (cancel speech when user interrupts).

Exit criteria:
- User can complete voice turn end-to-end (speak -> plan/response -> spoken output).
- Latency and errors are visible in telemetry logs.

### Phase P6 - Character Skins V0 (2-7 days)
Goal: make appearance system configurable without runtime code changes.

Tasks:
- [ ] `P6-T1` Finalize skin-pack manifest and loader contract.
- [ ] `P6-T2` Ship default skin pack with idle/talk/emotion assets.
- [ ] `P6-T3` Add UI skin selector and hot-swap support.

Exit criteria:
- Skins can be switched at runtime without restarting services.

### Phase P7 - V1 Hardening and Packaging (1-3 weeks)
Goal: make the product installable and operationally safe.

Tasks:
- [ ] `P7-T1` Add installer/distribution pipelines by OS.
- [ ] `P7-T2` Add first-run model/voice download workflow.
- [ ] `P7-T3` Implement crash recovery and service health panel.
- [ ] `P7-T4` Run privacy/safety verification pass.

Exit criteria:
- V1 build is installable, recoverable, and policy-compliant.

## Milestone Gates
- `M1` (after P2): typed chat UI working over IPC.
- `M2` (after P4): approved tool actions execute with audit logs.
- `M3` (after P5): local voice conversation stable.
- `M4` (after P6): skin packs hot-swappable.
- `M5` (after P7): packaged release candidate.

## Immediate Next Actions
- [ ] `N1` Create scaffolding for `ipc-hub`, `desktop-ui`, `agent-core`.
- [ ] `N2` Implement minimal envelope validation and routing smoke test.
- [ ] `N3` Build typed-chat vertical slice (`desktop-ui` -> `agent-core` -> `desktop-ui`).

## Roadmap Update Rules
- Every completed task must be checked and dated in this file.
- Any scope shift must update both roadmap tasks and referenced specs in the same session.
- New work must be attached to a phase task ID (`P#-T#`) before coding starts.
