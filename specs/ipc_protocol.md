# IPC Protocol Spec

Related roadmap tasks: `P1-T1`, `P1-T2`, `P1-T3`, `P1-T4`, `P3-T1`

## Transport
- Protocol: WebSocket
- Endpoint: `ws://127.0.0.1:17171/ws`
- Encoding: UTF-8 JSON
- Auth: first message must be `auth.hello`
- IDs: ULID or UUIDv7 for `id` and `trace_id`

## Envelope
```json
{
  "v": 1,
  "id": "01J...",
  "ts": "2026-02-16T12:34:56.789Z",
  "from": "desktop-ui",
  "to": "agent-core",
  "topic": "chat.user_message",
  "reply_to": null,
  "trace_id": "01J...",
  "payload": {}
}
```

## Required Topics
- `auth.hello`, `auth.ok`, `auth.error`
- `hb.ping`, `hb.pong`
- `chat.user_message`, `chat.assistant_plan`, `chat.assistant_message`
- `tool.execute`, `tool.results`
- `confirm.grant`
- `voice.capture.start`, `voice.stt.partial`, `voice.stt.final`, `voice.tts.speak`

## Conversation Flow
1. UI receives typed/voice input.
2. UI sends `chat.user_message` to `agent-core`.
3. `agent-core` returns either:
   - `chat.assistant_message` (no tools), or
   - `chat.assistant_plan` (steps + proposed tools + confirmation requirement).
4. UI obtains user confirmation for medium/high risk actions.
5. UI issues `confirm.grant` with scoped token.
6. `agent-core` sends `tool.execute` with `confirm_token`.
7. `automation-service` emits `tool.results`.
8. `agent-core` returns final assistant message; UI may trigger TTS.

## Validation Rules
- Reject messages without required envelope keys.
- Reject unknown topic versions (`v`).
- Reject unauthorized sender/topic combinations.
- Enforce TTL on confirmation tokens.
- Preserve `trace_id` end-to-end.

## Failure Semantics
- Schema failures return `*.error` with stable error codes.
- Timeout failures include retriable hints when safe.
- Service disconnects invalidate in-flight confirmations.
