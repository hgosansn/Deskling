# Deskling Character Demo

This is the MVP character demo - a simple, delightful desktop companion.

## What is it?

A floating stickman character that:
- Lives on your desktop (always on top)
- Can be dragged anywhere on screen
- Shows speech bubbles when clicked
- Has smooth idle and talking animations
- Works on Linux (Fedora), macOS, and Windows

## Running the Demo

```bash
cd apps/desktop-ui
npm install
npm run character
```

Or with dev tools:
```bash
npm run character:dev
```

## Interactions

- **Drag**: Click and drag anywhere on the window (except the character itself) to move it around
- **Click Character**: Click the stickman to see random messages in speech bubbles
- **Hover Character**: Hover over the stickman to see a zoom effect

## Features

- ✅ Transparent, frameless window
- ✅ Simple animated stickman sprite
- ✅ Speech bubble system
- ✅ Draggable around screen
- ✅ Idle bounce animation
- ✅ Talking animation when showing messages
- ✅ Click interactions

## Technical Details

- Built with Electron
- No backend services required (standalone)
- Uses CSS animations for smooth character movement
- SVG-based stickman character
- Webkit drag region for window dragging

## Next Steps (Post-MVP)

The full Deskling vision includes:
- Voice conversation (push-to-talk)
- LLM-powered responses
- Tool execution with confirmations
- Character skin customization
- Multi-service architecture

These features are implemented in the codebase but not part of the current MVP demo.
