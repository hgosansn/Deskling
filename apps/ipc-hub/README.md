# IPC Hub

WebSocket-based message router for inter-process communication.

## Responsibilities
- Loopback-only WebSocket endpoint (`127.0.0.1:17171`)
- Service registration and capability metadata
- Schema validation and message routing
- Heartbeat monitoring

## Related Specs
- `specs/architecture.md`
- `specs/ipc_protocol.md`

## Related Roadmap
- P1-T1: Build ipc-hub WebSocket server
- P1-T2: Implement auth handshake and service registration
- P1-T3: Implement heartbeat, routing, and request/response correlation
- P1-T4: Add message schema validation and structured errors
