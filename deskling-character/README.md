# Deskling Character - Rust Implementation

A delightful desktop character companion built with Rust using egui/eframe.

## Features

- ✨ Transparent, frameless window
- 🎯 Always-on-top floating character
- 🤸 Animated stickman sprite with smooth animations
- 💬 Speech bubble system (click character for messages)
- 🖱️ Draggable window
- 🎨 Hover zoom effect
- 🚀 Native performance with Rust

## Building

### Prerequisites

- Rust toolchain (1.70+)
- On Linux: `libxcb`, `libxkbcommon`, and `libwayland` development packages

### Linux (Fedora/RHEL)
```bash
sudo dnf install libxcb-devel libxkbcommon-devel wayland-devel
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev \
    libxkbcommon-dev libwayland-dev libssl-dev
```

### Build and Run

```bash
cd deskling-character
cargo build --release
cargo run --release
```

## Usage

1. **Launch the app**: `cargo run --release`
2. **Drag**: Click and drag anywhere on the window to move the character
3. **Chat**: Click the stickman character to see messages in speech bubbles
4. **Hover**: Hover over the character for a zoom effect
5. **Close**: Close the window or use Ctrl+C in terminal

## Technical Details

- **Framework**: egui/eframe (immediate mode GUI)
- **Graphics**: Custom stickman rendering with egui painter
- **Animations**: Smooth 60 FPS animations
  - Idle bounce (slower wave)
  - Talking bob (faster bounce when showing messages)
  - Hover zoom (1.1x scale)
- **Speech Bubbles**: 10 pre-defined messages, auto-hide after 3 seconds

## Interactions

The character responds to:
- **Click on character**: Shows next message
- **Hover over character**: Zooms in slightly
- **Drag window**: Move character anywhere on screen
- **Welcome message**: Automatically shows on startup

## Character States

- **Idle**: Gentle bouncing animation
- **Talking**: Faster bobbing when speech bubble is visible
- **Hover**: Scales up to 1.1x size

## Messages

Click the character to cycle through:
1. "Hi there! 👋"
2. "I'm Deskling, your desktop buddy!"
3. "Drag me anywhere you like!"
4. "Click me again for another message!"
5. "I can show text in speech bubbles!"
6. "Having fun yet? 😊"
7. "I'm a simple stickman for now!"
8. "This is the MVP demo in Rust!"
9. "More features coming soon!"
10. "Built with egui and Rust!"

## Performance

- Native binary with optimized release build
- ~60 FPS animations with minimal CPU usage
- Low memory footprint
- Fast startup time

## Differences from Electron Version

| Feature | Electron | Rust |
|---------|----------|------|
| Startup Time | ~2-3s | <0.5s |
| Memory Usage | ~100-150 MB | ~20-30 MB |
| CPU Usage | Higher | Lower |
| Bundle Size | ~100+ MB | <5 MB |
| Native Look | No | Yes |
| Cross-platform | ✅ | ✅ |

## Troubleshooting

### Black window on Linux
If you see a black window instead of transparency:
- Make sure your compositor supports transparency (e.g., GNOME, KDE)
- Try running with Wayland: `WINIT_UNIX_BACKEND=wayland cargo run --release`

### Window not staying on top
Some window managers may override the always-on-top flag. Check your WM settings.

### Build errors
Make sure you have all required development packages installed (see Prerequisites).
