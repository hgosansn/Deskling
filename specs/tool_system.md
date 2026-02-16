# Tool System Spec

Related roadmap tasks: `P3-T2`, `P3-T3`, `P4-T1`, `P4-T2`, `P4-T3`, `P4-T4`, `P4-T5`

## Design Goals
- Safe by default
- Structured and inspectable execution
- Reversible operations where possible
- Clear user consent model for risky actions

## Tool Definition Contract
Each tool definition must include:
- `name`
- `description`
- `args_schema` (JSON Schema)
- `risk` (`low | medium | high`)
- `confirmation` (`never | if_destructive | always`)
- `scopes` (paths/apps/network constraints)

Example:
```json
{
  "name": "files.move_glob",
  "description": "Move files matching patterns from one folder to another.",
  "risk": "medium",
  "confirmation": "if_destructive",
  "args_schema": {
    "type": "object",
    "properties": {
      "from": {"type": "string"},
      "patterns": {"type": "array", "items": {"type": "string"}},
      "to": {"type": "string"}
    },
    "required": ["from", "patterns", "to"]
  }
}
```

## Confirmation Policy
- `low`: execute directly unless local policy forces confirmation.
- `medium`: require `confirm_token` when operation mutates state.
- `high`: always require confirmation with explicit scope and short expiry.

`confirm_token` requirements:
- tied to `trace_id`
- includes allowed tools and scopes
- expires by TTL
- single-use unless explicitly marked reusable

## Initial Tool Set (V1)
- `clipboard.read`
- `clipboard.write`
- `notify.send`
- `apps.open`
- `files.list_dir`
- `files.search`
- `files.read_text`
- `files.write_text`
- `files.ensure_dir`
- `browser.open_url` (Playwright-backed)

Deferred for later hardening:
- `shell.run` (opt-in only)
- arbitrary mouse/keyboard automation outside scoped tasks

## Execution Lifecycle
1. Agent proposes tool calls in `chat.assistant_plan`.
2. UI captures user approval if required.
3. Agent sends `tool.execute` to automation-service.
4. Automation-service validates schema + policy + confirmation token.
5. Tool executes and emits `tool.results` with audit metadata.

## Audit Requirements
Every tool call must log:
- `trace_id`
- `call_id`
- tool name + args hash
- policy decision (allowed/blocked + reason)
- execution result (`ok`/`error`) and summary
- start/end timestamps
