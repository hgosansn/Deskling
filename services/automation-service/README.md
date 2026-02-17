# Automation Service

Safe tool execution service with audit logging.

## Responsibilities
- Tool execution with policy checks
- Confirmation token enforcement
- Scoped path/network/app constraints
- Structured audit event emission

## Tech Stack
- Python 3.10+
- Playwright for browser automation
- WebSocket client for IPC

## Related Specs
- `specs/architecture.md`
- `specs/tool_system.md`

## Related Roadmap
- P4-T1: Implement low-risk tools (clipboard, notify, apps.open)
- P4-T2: Implement file tools with allowlisted paths
- P4-T3: Enforce confirm-token validation and scope expiry
- P4-T4: Add structured audit events
- P4-T5: Integrate Playwright (browser.open_url)
