# Product Scope

Related roadmap tasks: `P0-T1`, `P2-T1`, `P3-T1`, `P5-T1`, `P6-T1`, `P7-T5`, `P7-T7`, `P8-T1`, `P9-T1`

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
- Fedora GNOME as the first required shipping target
- macOS/Windows compatibility as final post-MVP parity stage
- Local-first operation with optional future remote providers

## Non-Goals (V1)
- Fully autonomous destructive actions
- Always-on wake word enabled by default
- Fully dynamic real-time avatar generation
- Mandatory cloud model dependency
- Token launch as a hard dependency for core assistant functionality

## Post-V1 Expansion Themes
- Utility-token economics for AI usage and creator marketplace (`specs/tokenomics.md`)
- Optional staking/perk mechanics with compliance-gated rollout

## Distribution Experience
- Provide a promotional product page with:
- download links by platform
- direct links to the Deskling marketplace

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
