# Specs

This folder is the product context source of truth.
`ROADMAP.md` defines sequencing and status; these specs define behavior and constraints.

## Read Order (MVP Focus)
1. `ROADMAP.md` - current priorities and status
2. `specs/mvp_scope.md` - **MVP character demo scope (current focus)**
3. `specs/project_scope.md` - full product vision (post-MVP)
4. `specs/architecture.md` - multi-service architecture (preserved)
5. `specs/ipc_protocol.md` - IPC protocol (preserved)
6. `specs/tool_system.md` - tool execution system (preserved)

## Sync Rules
- Every roadmap task must map to at least one spec section.
- Any scope or behavior change must update both roadmap and affected specs in the same session.
- Specs should reference roadmap IDs (`P#-T#` or `MVP-T#`) for traceability.

## Current Specs

### Active MVP Specs
- `specs/mvp_scope.md` - **MVP character demo: problem, goals, non-goals, success criteria**

### Preserved Full Product Specs
- `specs/project_scope.md` - full product problem, goals, non-goals, success criteria
- `specs/architecture.md` - services, boundaries, repository baseline
- `specs/ipc_protocol.md` - message envelopes, topics, validation, failures
- `specs/tool_system.md` - tool schema contract, safety policy, initial tool catalog
