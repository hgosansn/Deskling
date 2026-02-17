# Architecture Spec

Related roadmap tasks: `P0-T1`, `P1-T1`, `P2-T3`, `P3-T4`, `P4-T4`, `P10-T1`, `P10-T8`

## System Topology
Multi-process local architecture with a single IPC hub:
- `desktop-ui` (Tauri): overlay, chat bubble, confirmations, settings
- `ipc-hub` (Rust): local message bus, auth, routing, heartbeat
- `agent-core` (Rust): planning, remote model interface, tool proposal generation
- `automation-service` (Rust): executes tools under policy and confirmation
- `voice-service` (Rust): STT/TTS provider adapters and audio control
- `skin-service` (optional Rust): skin catalog and generation hooks

Rule: no direct service-to-service calls except through `ipc-hub`.

## Repository Baseline (target)
- `apps/desktop-ui/`
- `apps/ipc-hub/`
- `services/agent-core/`
- `services/automation-service/`
- `services/voice-service/`
- `services/skin-service/` (optional)
- `shared/schemas/`
- `configs/`
- `scripts/`
- `specs/`

## Service Responsibilities
### ipc-hub
- loopback-only WebSocket endpoint
- service registration and capability metadata
- schema validation and routing
- heartbeat monitoring

### desktop-ui
- overlay rendering and interaction
- user input capture (typed + push-to-talk triggers)
- display of plan/confirmation flow
- state transitions and status display

### agent-core
- user intent handling and planning
- model inference orchestration
- tool proposal generation (not execution)
- response composition and fallback behavior

### automation-service
- tool execution with policy checks
- confirmation token enforcement
- scoped path/network/app constraints
- structured audit event emission

### voice-service
- microphone capture and transcript generation
- TTS generation and playback controls
- barge-in interruption handling
- remote-provider-only inference adapters in v1 (no local model runtimes bundled)

### skin-service
- skin listing, install/uninstall, metadata lookup
- optional remote generation hooks (offline generation pipelines are post-v1)

## Cross-Cutting Constraints
- Local-first security model
- Trace ID propagation across every message
- JSON-schema-validated boundaries
- Config-driven permissions and model paths
- Minimal runtime dependencies in release bundle (Rust services + Tauri host; no Python runtime requirement)
- Structured JSON logs per `specs/logging_conventions.md`
