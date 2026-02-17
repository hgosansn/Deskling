# Architecture Spec

Related roadmap tasks: `P0-T1`, `P1-T1`, `P2-T3`, `P3-T4`, `P4-T4`

## System Topology
Multi-process local architecture with a single IPC hub:
- `desktop-ui` (Tauri): overlay, chat bubble, confirmations, settings
- `ipc-hub` (Python): local message bus, auth, routing, heartbeat
- `agent-core` (Python): planning, model interface, tool proposal generation
- `automation-service` (Python): executes tools under policy and confirmation
- `voice-service` (Python): STT/TTS pipeline and audio control
- `skin-service` (optional Python): skin catalog and generation hooks

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

### skin-service
- skin listing, install/uninstall, metadata lookup
- optional ComfyUI integration for offline generation pipelines

## Cross-Cutting Constraints
- Local-first security model
- Trace ID propagation across every message
- JSON-schema-validated boundaries
- Config-driven permissions and model paths
- Structured JSON logs per `specs/logging_conventions.md`
