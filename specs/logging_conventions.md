# Logging Conventions

Related roadmap tasks: `P0-T4`, `P4-T4`

## Goals
- Structured logs across all services
- Trace ID included on every operational event
- Machine-readable format for audit and debugging

## Baseline Format
Services emit one JSON object per line with these keys:
- `ts`: UTC timestamp in ISO-8601
- `level`: `debug|info|warning|error`
- `service`: service identifier (`ipc-hub`, `agent-core`, etc.)
- `event`: stable event name
- `trace_id`: request/workflow trace identifier

Optional fields:
- event-specific metadata (`port`, `state`, `policy`, `result`, ...)

## Implementation Baseline
- Shared Python helper: `shared/python/tasksprite_common/trace_logging.py`
- Stub services use the helper and emit startup/heartbeat/stop events.

## Usage Rules
- Generate a trace ID at request ingress; preserve it through all downstream logs.
- Never log secrets or raw credential material.
- Keep event names short and stable for filtering (`service.start`, `policy.ready`, `tool.result`).
