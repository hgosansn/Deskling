# Project Roadmap - Cross-Platform Voice Desktop Mate

Last updated: 2026-02-17

## Purpose
This roadmap is the execution plan for building the product. It is intentionally concise and phase-driven.
Detailed design and implementation rules live in `specs/`.

## Canonical Context (read before implementation)
- `ROADMAP.md` - sequencing, priorities, milestones, status
- `specs/project_scope.md` - product definition, goals, non-goals, success criteria
- `specs/architecture.md` - system architecture, service boundaries, repository layout
- `specs/ipc_protocol.md` - inter-process protocol and conversation flows
- `specs/tool_system.md` - tool contracts, risk model, confirmation policy, initial tool set
- `specs/logging_conventions.md` - structured logs and trace-id handling rules
- `specs/tokenomics.md` - DSL utility-token policy, distribution, and rollout constraints
- `specs/stickman_mvp.md` - Tauri-only Fedora MVP for desktop stickman behavior and extensible skin/animation hooks

## Pre-Start Decisions (Locked)
These are committed choices for v1 unless explicitly changed in roadmap updates.

- `D1` Runtime split: multi-process local system (`desktop-ui`, `ipc-hub`, `agent-core`, `voice-service`, `automation-service`, optional `skin-service`).
- `D2` UI stack: Tauri for v1 delivery speed and native footprint.
- `D3` Core service language: Rust for all production services (`ipc-hub`, `agent-core`, `automation-service`, `voice-service`, `skin-service`).
- `D4` IPC transport: local WebSocket hub on loopback only (`127.0.0.1`), JSON envelopes, heartbeat, token auth.
- `D5` LLM runtime: remote-provider-first abstraction (HTTP APIs); no local model runtime in v1.
- `D6` STT: remote-provider-first; local STT runtimes are not in v1 scope.
- `D7` TTS: remote-provider-first; local TTS runtimes are not in v1 scope.
- `D8` Browser automation: Playwright as default web execution path.
- `D9` Desktop automation safety: confirmation-token gate for medium/high risk actions.
- `D10` Character system: skin-pack format for v1; live generation is v1.5+.
- `D11` Initial release mode: push-to-talk first; wake-word deferred.
- `D12` Data/privacy baseline: local-first storage, audit logs for tool actions, no secret leakage in assistant responses.
- `D13` Platform priority: Fedora Linux (GNOME) is the primary development and MVP qualification environment; macOS/Windows parity is post-MVP.

## Decision Change Log
- `2026-02-17` Architecture pivot approved: Rust-only service rewrite and no local inference baseline. Packaging size, runtime simplicity, and cross-platform release stability are now prioritized over mixed-runtime iteration speed.

## Out of Scope for V1
- Always-on wake-word by default
- Fully autonomous destructive actions without confirmation
- Real-time generated 3D avatar creation
- Cloud dependency as required path
- Local model/runtime inference stacks (for example Ollama, Whisper.cpp, Piper) in v1

## Phase Plan

### Phase P0 - Setup and Governance (1-2 days)
Goal: create the delivery baseline before writing feature code.

Tasks:
- [x] `P0-T1` Define monorepo skeleton and service directories per `specs/architecture.md`. (Done 2026-02-16)
- [x] `P0-T2` Add local config templates (`configs/default.toml`, `configs/permissions.toml`). (Done 2026-02-16)
- [x] `P0-T3` Add scripts for local orchestration (`scripts/dev-up.sh`, `scripts/build-all.sh`). (Done 2026-02-16)
- [x] `P0-T4` Implement logging/trace-id conventions used across all services. (Done 2026-02-16)

Exit criteria:
- Single command can start hub + one stub service + UI shell.
- All new modules follow the shared naming and config conventions.

### Phase P1 - IPC Backbone (2-4 days)
Goal: establish reliable local communication and routing.

Tasks:
- [x] `P1-T1` Build `ipc-hub` WebSocket server with loopback-only binding. (Done 2026-02-16)
- [x] `P1-T2` Implement auth handshake and service registration. (Done 2026-02-16)
- [x] `P1-T3` Implement heartbeat, routing, and request/response correlation. (Done 2026-02-16)
- [x] `P1-T4` Add message schema validation and structured errors. (Done 2026-02-16)

Exit criteria:
- UI and 2 services can connect and exchange validated messages.
- Lost heartbeat disconnect and reconnect path is observable in logs.

### Phase P2 - Desktop UI Shell (3-6 days)
Goal: deliver visible assistant shell with state transitions.

Tasks:
- [x] `P2-T1` Create transparent always-on-top overlay window. (Done 2026-02-16)
- [x] `P2-T2` Add draggable character and chat bubble. (Done 2026-02-16)
- [x] `P2-T3` Implement state machine (`idle`, `listen`, `think`, `speak`, `run`, `error`). (Done 2026-02-16)
- [x] `P2-T4` Build confirmation dialog UI for risky tool actions. (Done 2026-02-16)
- [x] `P2-T5` Add base settings panel (audio device, model paths, voice). (Done 2026-02-16)

Exit criteria:
- Operator can send typed messages and receive responses through IPC.
- Confirmation UX blocks risky actions by default.

### Phase P3 - Agent Core V0 (3-7 days)
Goal: produce structured plans and tool requests safely.

Tasks:
- [x] `P3-T1` Implement agent input/output contract from `specs/ipc_protocol.md`. (Done 2026-02-16)
- [x] `P3-T2` Add planner output (`chat.assistant_plan`) with risk labeling. (Done 2026-02-16)
- [x] `P3-T3` Add tool call proposal format and confirmation requirements. (Done 2026-02-16)
- [x] `P3-T4` Add failure handling and retry suggestion templates. (Done 2026-02-16)

Exit criteria:
- Agent can respond to typed requests with clear plan and structured tool proposals.
- No direct execution path from agent-core to OS actions.

### Phase P4 - Automation Service V0 (4-10 days)
Goal: execute approved tools with auditability and hard safety boundaries.

Tasks:
- [x] `P4-T1` Implement low-risk tools (`clipboard.*`, `notify.send`, `apps.open`). (Done 2026-02-16)
- [x] `P4-T2` Implement file tools with allowlisted paths and overwrite checks. (Done 2026-02-16)
- [x] `P4-T3` Enforce confirm-token validation and scope expiry. (Done 2026-02-16)
- [x] `P4-T4` Add structured audit events for every tool execution. (Done 2026-02-16)
- [x] `P4-T5` Integrate Playwright starter action (`browser.open_url`). (Done 2026-02-16)

Exit criteria:
- Tool execution requires policy compliance and returns traceable results.
- Audit log can reconstruct who asked for what and what changed.

### Phase P5 - Voice Service V0 (4-10 days)
Goal: add local voice conversation loop.

Tasks:
- [x] `P5-T1` Implement push-to-talk capture and final transcript events. (Done 2026-02-16)
- [x] `P5-T2` Integrate STT adapter (Whisper.cpp or faster-whisper). (Done 2026-02-16)
- [x] `P5-T3` Integrate Piper TTS playback. (Done 2026-02-16)
- [x] `P5-T4` Add barge-in (cancel speech when user interrupts). (Done 2026-02-16)

Exit criteria:
- User can complete voice turn end-to-end (speak -> plan/response -> spoken output).
- Latency and errors are visible in telemetry logs.

### Phase P6 - Character Skins V0 (2-7 days)
Goal: make appearance system configurable without runtime code changes.

Tasks:
- [x] `P6-T1` Finalize skin-pack manifest and loader contract. (Done 2026-02-16)
- [x] `P6-T2` Ship default skin pack with idle/talk/emotion assets. (Done 2026-02-16)
- [x] `P6-T3` Add UI skin selector and hot-swap support. (Done 2026-02-16)

Exit criteria:
- Skins can be switched at runtime without restarting services.

### Phase P7 - Fedora MVP Qualification and Packaging (1-3 weeks)
Goal: make the product installable and operationally safe on Fedora GNOME as the first shipping target.

Tasks:
- [x] `P7-T0` Deliver Tauri-only stickman desktop MVP on Fedora (borderless UI, moving character, contextual local messages, skin/animation extension points). (Done 2026-02-18)
- [ ] `P7-T1` Add Fedora packaging/distribution pipeline for MVP delivery. (in progress)
- [ ] `P7-T2` Add first-run model/voice download workflow.
- [ ] `P7-T3` Implement crash recovery and service health panel.
- [ ] `P7-T4` Run privacy/safety verification pass.
- [ ] `P7-T5` Add Fedora GNOME qualification checklist (window behavior, audio I/O, tray/menu, permissions).
- [ ] `P7-T6` Run and document Fedora GNOME install + smoke test flow as release baseline.
- [ ] `P7-T7` Create promotional download page with platform download links and marketplace entry links.
- [ ] `P7-T8` Add LLM-backed contextual speech generation for stickman messages after MVP local-rules baseline.
- [ ] `P7-T9` Add direct interaction layer (user intents, follow-ups, and richer response actions) after MVP.

Exit criteria:
- Fedora GNOME MVP build is installable, recoverable, and policy-compliant.
- Public download page exists with clear install paths and marketplace navigation.

### Phase P8 - Cross-Platform Parity (3-7 days)
Goal: extend the Fedora-qualified MVP to macOS and Windows compatibility as final follow-up.

Tasks:
- [ ] `P8-T1` Add macOS/Windows compatibility guardrails in CI/build scripts (no Linux-only assumptions in core paths).
- [ ] `P8-T2` Add installer/distribution pipelines for macOS and Windows.
- [ ] `P8-T3` Run platform qualification smoke tests on macOS and Windows.
- [ ] `P8-T4` Close or backlog remaining macOS/Windows parity gaps with owner + priority.

Exit criteria:
- macOS and Windows have documented install/smoke-test paths after Fedora MVP.
- Remaining parity risks are explicitly tracked and prioritized.

### Phase P9 - Tokenomics and Ecosystem Economics (1-2 weeks)
Goal: define and launch a utility-first economic model for AI usage and creator marketplace flows after platform foundations are stable.

Tasks:
- [x] `P9-T1` Finalize DSL tokenomics specification and legal/compliance constraints by jurisdiction. (Done 2026-02-16)
- [ ] `P9-T2` Define compute-credit conversion model (fiat <-> DSL) with treasury and reserve accounting.
- [ ] `P9-T3` Define marketplace settlement model for creators (fees, payouts, dispute handling, anti-abuse controls).
- [ ] `P9-T4` Define staking/perk policy and optional burn mechanics with sustainability simulations.
- [ ] `P9-T5` Publish phased rollout plan (off-chain first, optional on-chain upgrade path) with risk gates.

Exit criteria:
- Token utility, supply policy, vesting, and fee flows are documented and approved.
- Legal/compliance review checklist exists for the initial launch jurisdictions.
- Implementation backlog is split into post-MVP epics with owners and sequencing.

### Phase P10 - Rust Rewrite and Runtime Simplification (2-4 weeks)
Goal: remove non-Rust runtime dependencies from the product path and run all core services in Rust while keeping Tauri UI and tokenomics constraints unchanged.

Tasks:
- [x] `P10-T0` Approve Rust-only/no-local-inference architecture pivot and synchronize roadmap/spec baselines. (Done 2026-02-17)
- [ ] `P10-T1` Rewrite `ipc-hub` in Rust with feature parity (auth, heartbeat, routing, schema validation, structured errors).
- [ ] `P10-T2` Rewrite `agent-core` in Rust with the same IPC contracts and risk-labeled planning outputs.
- [ ] `P10-T3` Rewrite `automation-service` in Rust with existing confirmation-token and audit requirements.
- [ ] `P10-T4` Rewrite `voice-service` in Rust using remote-provider adapters only (no local inference runtimes bundled).
- [ ] `P10-T5` Rewrite `skin-service` in Rust (or merge into another Rust service if lower operational overhead).
- [ ] `P10-T6` Replace legacy dev/test scripts with Rust binaries and cargo-based checks.
- [ ] `P10-T7` Remove non-Rust runtime dependencies from packaging and CI; verify reduced bundle footprint and simpler install path.
- [ ] `P10-T8` Re-run Fedora qualification and cross-platform smoke tests after Rust rewrite.

Exit criteria:
- No production runtime dependency outside Rust services remains.
- Build/test/deploy path is cargo + Node/Tauri only.
- Bundle size and install complexity are reduced versus the previous baseline.
- IPC/tool/confirmation behavior remains backward-compatible with current schemas and policies.

## Milestone Gates
- `M1` (after P2): typed chat UI working over IPC. (Reached 2026-02-16)
- `M2` (after P4): approved tool actions execute with audit logs. (Reached 2026-02-16)
- `M3` (after P5): local voice conversation stable. (Reached 2026-02-16)
- `M4` (after P6): skin packs hot-swappable. (Reached 2026-02-16)
- `M5` (after P7): Fedora GNOME MVP qualified release candidate.
- `M6` (after P8): macOS/Windows compatibility baseline established.
- `M7` (after P9): tokenomics and marketplace economics launch plan approved.
- `M8` (after P10): Rust-only runtime baseline validated for Fedora and cross-platform follow-up.

## Immediate Next Actions
- [x] `N1` Create scaffolding for `ipc-hub`, `desktop-ui`, `agent-core`. (Done 2026-02-16)
- [x] `N2` Implement minimal envelope validation and routing smoke test. (Done 2026-02-16)
- [x] `N3` Build typed-chat vertical slice (`desktop-ui` -> `agent-core` -> `desktop-ui`). (Done 2026-02-16)
- [x] `N4` Reconcile divergent `main` histories while preserving locked decisions from `D2` (Tauri) and tokenomics references in `specs/tokenomics.md`. (Done 2026-02-17)
- [x] `N5` Rebaseline roadmap/specs to Rust-only services and no local inference strategy. (Done 2026-02-17)

## Roadmap Update Rules
- Every completed task must be checked and dated in this file.
- Any scope shift must update both roadmap tasks and referenced specs in the same session.
- New work must be attached to a phase task ID (`P#-T#`) before coding starts.
