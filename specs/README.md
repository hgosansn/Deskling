# Specs

This folder is the product context source of truth.
`ROADMAP.md` defines sequencing and status; these specs define behavior and constraints.

## Read Order
1. `ROADMAP.md`
2. `specs/project_scope.md`
3. `specs/architecture.md`
4. `specs/ipc_protocol.md`
5. `specs/tool_system.md`

## Sync Rules
- Every roadmap task must map to at least one spec section.
- Any scope or behavior change must update both roadmap and affected specs in the same session.
- Specs should reference roadmap IDs (`P#-T#`) for traceability.

## Current Specs
- `specs/project_scope.md` - problem, goals, non-goals, success criteria
- `specs/architecture.md` - services, boundaries, repository baseline
- `specs/ipc_protocol.md` - message envelopes, topics, validation, failures
- `specs/tool_system.md` - tool schema contract, safety policy, initial tool catalog
