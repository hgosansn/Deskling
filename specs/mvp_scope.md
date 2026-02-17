# MVP Scope - Desktop Character Companion

Related roadmap tasks: `MVP-T1` through `MVP-T8`
Last updated: 2026-02-17

## Problem Statement
Users want to see a delightful, visually appealing desktop character companion as a demo, not a complex multi-service voice assistant. The MVP should showcase the character interaction experience.

## MVP Product Definition
A floating desktop character application that:
- displays a simple animated stickman character
- can be dragged around the screen freely
- shows speech bubbles with text messages
- has minimal interactive behaviors (click, hover, idle animations)
- runs as a standalone Electron app on Fedora (and other platforms)

## MVP Goals
- **Visual appeal**: Character should be cute and engaging
- **Simplicity**: No complex service dependencies for demo
- **Interactivity**: Basic drag and text display working smoothly
- **Cross-platform**: Works on Linux (Fedora primary), macOS, Windows

## MVP Non-Goals
- Voice conversation pipeline
- LLM integration or AI responses
- Complex multi-service architecture (preserved but not active)
- Tool execution or automation features
- Skin customization system

## MVP Success Criteria
- Character window launches successfully on Fedora
- User can drag character to any screen position
- Speech bubbles display text properly
- Character has at least 2-3 animated states (idle, talking, moving)
- Visual design is appealing and not generic
- Application runs smoothly without crashes

## MVP User Experience Principles
- **Delightful first**: Focus on making the character charming and fun
- **Immediate feedback**: Character responds to interactions instantly
- **Minimal UI**: Let the character be the interface
- **Smooth animations**: No janky movements or transitions
- **Always accessible**: Character stays on top but not intrusive

## Technical Approach (MVP)
- **Standalone mode**: Desktop UI runs without IPC hub dependency for demo
- **Simple graphics**: Canvas-based stickman character (SVG or drawn)
- **State machine**: idle, talking, dragging states
- **Speech bubbles**: CSS-based bubbles positioned near character
- **Minimal interactions**: Click for random message, drag to move

## Post-MVP Features (Preserved in Codebase)
The following features are implemented but not part of the MVP demo focus:
- IPC hub and multi-service architecture
- Agent-core for planning and tool proposals
- Automation service with tool execution
- Voice service integration
- Advanced confirmation flows

These features remain in the repository for future development but are not required for the MVP demo.
