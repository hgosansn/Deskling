# Deskling Character Demo - Visual Documentation

## MVP Demo Overview

The Deskling character demo is a delightful desktop companion application featuring:
- A simple animated stickman character
- Speech bubbles for text display
- Drag-and-drop window positioning
- Smooth animations and interactions

## Visual Layout

```
┌────────────────────────────────────┐
│  Transparent Window (300x400px)    │
│  Always on Top, Frameless          │
│                                    │
│     ╭─────────────────────╮       │
│     │  Hi there! 👋       │       │  ← Speech Bubble
│     │  I'm your buddy!    │       │    (appears above character)
│     ╰─────────┬───────────╯       │
│               │                    │
│               ▼                    │
│                                    │
│            ●●●●●                   │  ← Stickman Head
│           ● O O ●                  │    (with eyes & smile)
│            ● ‿ ●                   │
│             ●●●                    │
│                                    │
│              │                     │  ← Body
│              │                     │
│          ╱   │   ╲                 │  ← Arms
│         ╱    │    ╲                │
│              │                     │
│             ╱ ╲                    │  ← Legs
│            ╱   ╲                   │
│           ╱     ╲                  │
│          ¯       ¯                 │  ← Feet
│                                    │
│   [Drag me around!]                │  ← Status hint
│                                    │    (fades after 3 sec)
└────────────────────────────────────┘
```

## Character States

### 1. Idle State
- Character bounces gently up and down
- Smooth 2-second animation loop
- Eyes follow a subtle movement pattern

### 2. Talking State
- Activated when speech bubble appears
- Character bobs faster (0.5-second loop)
- Slight scale increase (1.05x)

### 3. Hover State
- Mouse hover triggers zoom effect
- Character scales to 1.1x
- Smooth 0.2-second transition

## Speech Bubble System

The speech bubble features:
- **Position**: Above character, centered
- **Style**: White background with black border, rounded corners
- **Animation**: Fades in smoothly over 0.3 seconds
- **Duration**: Displays for 3 seconds before fading out
- **Pointer**: Small triangular pointer points down to character

### Sample Messages
When you click the character, it cycles through these messages:
1. "Hi there! 👋"
2. "I'm Deskling, your desktop buddy!"
3. "Drag me anywhere you like!"
4. "Click me again for another message!"
5. "I can show text in speech bubbles!"
6. "Having fun yet? 😊"
7. "I'm a simple stickman for now!"
8. "This is the MVP demo!"
9. "More features coming soon!"
10. "You can build amazing things with Electron!"

## Interaction Guide

### How to Drag
1. Click anywhere on the window background (the drag region)
2. Hold and move mouse to reposition the character
3. Release to drop at new location
4. Character stays at new position until moved again

### How to Chat
1. Click directly on the stickman character
2. Speech bubble appears with a message
3. Click again for next message in cycle
4. Messages rotate through the full list

### How to Hover
1. Move mouse over the stickman
2. Character smoothly zooms in
3. Move away to return to normal size

## Technical Details

### Window Properties
- **Size**: 300x400 pixels
- **Transparency**: True (see-through background)
- **Frame**: None (frameless window)
- **Always on Top**: Yes
- **Resizable**: No (fixed size for MVP)

### Character Graphics
- **Format**: SVG (Scalable Vector Graphics)
- **Size**: 120x180 pixels
- **Colors**: Simple black (#333) with white eyes
- **Style**: Clean, minimalist stickman design

### Animations
- **Idle Bounce**: CSS keyframe animation, 2s duration, infinite loop
- **Talk Bob**: CSS keyframe animation, 0.5s duration, infinite loop while talking
- **Hover Zoom**: CSS transition, 0.2s duration, scale transform

### Platform Compatibility
✅ **Linux** (Fedora, Ubuntu, Debian, etc.)
✅ **macOS** (10.13+)
✅ **Windows** (10, 11)

## Color Scheme

- **Character Body**: #333333 (Dark gray)
- **Character Outline**: #000000 (Black)
- **Eyes**: #FFFFFF (White) with #000000 pupils
- **Speech Bubble Background**: rgba(255, 255, 255, 0.95) (White, 95% opacity)
- **Speech Bubble Border**: #333333 (Dark gray)
- **Speech Bubble Shadow**: rgba(0, 0, 0, 0.2) (Subtle drop shadow)

## Screenshots

### Main View
```
The character appears as a friendly stickman with:
- Round head with two eyes and a smile
- Simple straight body line
- Two arms extended outward
- Two legs in standing position
- Clean black lines on transparent background
```

### With Speech Bubble
```
When clicked, a white rounded rectangle appears above
the character containing text. A small triangle points
down from the bubble to the character, creating a
classic comic-style speech effect.
```

### Idle Animation
```
The character gently bounces up and down, creating
a lively "breathing" effect even when idle. This
subtle motion makes the character feel alive and
engaging without being distracting.
```

## Demo Workflow

1. **Launch**: Run `npm run character` in apps/desktop-ui
2. **Window Appears**: Transparent window with stickman appears
3. **Welcome Message**: After 0.5s, first speech bubble shows
4. **Status Hint**: "Drag me around!" label shows for 3 seconds
5. **Ready for Interaction**: User can now drag and click
6. **Click to Chat**: Each click shows next message
7. **Drag to Move**: Window follows mouse during drag
8. **Always Visible**: Stays on top of other windows

## Future Enhancements (Post-MVP)

The current MVP is intentionally simple. Future versions could add:
- [ ] More elaborate character designs (different skins)
- [ ] Voice integration (text-to-speech for bubbles)
- [ ] Multiple character poses
- [ ] Background themes
- [ ] User-customizable messages
- [ ] System tray integration
- [ ] Multiple characters on screen
- [ ] Character-to-character conversations

## File Structure

```
apps/desktop-ui/
├── main-character.js          # Electron main process
├── package.json               # npm scripts: "character" command
├── renderer/
│   └── character.html         # UI with stickman SVG & interactions
├── README-CHARACTER.md        # User documentation
└── test-character.js          # Validation tests
```

## Running the Demo

```bash
# Install dependencies
cd apps/desktop-ui
npm install

# Run character demo
npm run character

# Run with developer tools (for debugging)
npm run character:dev
```

## Expected Behavior

When you run the demo:
1. ✅ A small transparent window appears
2. ✅ Stickman character is visible and bouncing
3. ✅ Welcome message shows in speech bubble
4. ✅ Window can be dragged around screen
5. ✅ Clicking character shows different messages
6. ✅ Window stays on top of other applications
7. ✅ No console errors in developer tools

## Testing Checklist

- [x] Window launches successfully
- [x] Character SVG renders correctly
- [x] Idle animation plays smoothly
- [x] Speech bubble appears and fades correctly
- [x] Click interaction cycles through messages
- [x] Drag functionality works across entire window
- [x] Hover effect scales character properly
- [x] Window stays always-on-top
- [x] No JavaScript errors in console
- [x] Works on Linux (tested on Ubuntu)

---

**Note**: This is the MVP demo. The full Deskling product includes voice
interaction, LLM responses, and tool execution, but those features are
preserved in the codebase and not part of this visual demo.
