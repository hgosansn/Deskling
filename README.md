# Deskling

Desktop character companion built with Tauri.

## Quick Start

```bash
cd apps/desktop-ui/src-tauri
cargo tauri dev
```

## Build for Production

```bash
cd apps/desktop-ui/src-tauri
cargo tauri build
```

## Features

- Transparent, frameless, always-on-top window
- Animated stickman character
- Speech bubbles with messages
- Draggable window
- Click character for different messages
- Hover for zoom effect

## Structure

```
apps/desktop-ui/
├── index.html          # Character UI
└── src-tauri/         # Tauri Rust backend
    ├── Cargo.toml
    ├── tauri.conf.json
    └── src/main.rs
```

## Requirements

- Rust (latest stable)
- Node.js (for Tauri CLI)

Install Tauri CLI:
```bash
cargo install tauri-cli
```

## Platform Support

- Linux
- macOS
- Windows
