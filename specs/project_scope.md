# Product Scope

Related roadmap tasks: `P0-T1`, `P2-T1`, `P3-T1`, `P5-T1`, `P6-T1`

## Problem Statement
Users need a lightweight desktop assistant that can hear, respond, and execute practical desktop/web tasks with explicit safety boundaries and local-first privacy.

## Product Definition
A floating desktop character assistant that:
- accepts typed and voice input
- responds with text and local speech
- proposes plans before medium/high risk actions
- executes approved tools through a dedicated automation service
- supports skin-pack based appearance switching

## Goals (V1)
- Reliable typed and voice interaction loop
- Safe and auditable tool execution
- Cross-platform baseline (Windows, macOS, Linux)
- Local-first operation with optional future remote providers

## Non-Goals (V1)
- Fully autonomous destructive actions
- Always-on wake word enabled by default
- Fully dynamic real-time avatar generation
- Mandatory cloud model dependency

## Success Criteria
- End-to-end typed interaction available in UI with confirmable tool plans
- End-to-end voice interaction (push-to-talk) with interruptible TTS
- Tool audit events include trace IDs and execution outcomes
- Appearance hot-swap works without process restart

## User Experience Principles
- Plan first for risky actions
- Minimal confirmation friction for low-risk operations
- Clear state visibility (`idle`, `listen`, `think`, `speak`, `run`, `error`)
- Transparent summaries of changes after actions complete
