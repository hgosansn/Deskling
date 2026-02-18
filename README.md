# Deskling

Desktop character companion built with Tauri.

## Quick Start

### Automated Setup (Linux/macOS)
```bash
# Run the setup script to install system dependencies
./setup-deps.sh

# Install Rust if not already installed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
cargo install tauri-cli

# Run the app
cd apps/desktop-ui/src-tauri
cargo tauri dev
```

### Manual Setup
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

### Core Requirements
- **Rust** (latest stable) - [Install Rust](https://rustup.rs/)
- **Tauri CLI** - Install with: `cargo install tauri-cli`

### System Dependencies

Tauri requires system libraries to build. Install the following based on your platform:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
  pkg-config \
  libglib2.0-dev \
  libgtk-3-dev \
  libwebkit2gtk-4.1-dev \
  libappindicator3-dev \
  librsvg2-dev \
  patchelf
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install -y \
  pkg-config \
  glib2-devel \
  gtk3-devel \
  webkit2gtk4.1-devel \
  libappindicator-gtk3-devel \
  librsvg2-devel \
  patchelf
```

#### Arch Linux
```bash
sudo pacman -S --needed \
  pkg-config \
  glib2 \
  gtk3 \
  webkit2gtk-4.1 \
  libappindicator-gtk3 \
  librsvg \
  patchelf
```

#### macOS
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

#### Windows
No additional dependencies needed. Make sure you have Visual Studio Build Tools or Visual Studio with C++ workload installed.

## Platform Support

- Linux (Ubuntu, Fedora, Arch, etc.)
- macOS
- Windows

## Troubleshooting

### Build Error: `glib-2.0` not found

**Error message:**
```
The system library `glib-2.0` required by crate `glib-sys` was not found.
The file `glib-2.0.pc` needs to be installed and the PKG_CONFIG_PATH environment variable must contain its parent directory.
```

**Solution:**
Install the system dependencies for your platform (see [System Dependencies](#system-dependencies) section above).

### Build Error: `webkit2gtk-4.1` not found

**Solution:**
- **Ubuntu/Debian:** Install `libwebkit2gtk-4.1-dev`
- **Fedora:** Install `webkit2gtk4.1-devel`
- **Arch:** Install `webkit2gtk-4.1`

### Build Error: Missing C++ compiler

**Solution:**
- **Linux:** Install `build-essential` (Debian/Ubuntu) or `gcc-c++` (Fedora)
- **macOS:** Run `xcode-select --install`
- **Windows:** Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

### Runtime Error: Window doesn't appear

**Solution:**
Make sure you have a display server running (X11 or Wayland on Linux).

For more help, see the [Tauri documentation](https://tauri.app/v1/guides/getting-started/prerequisites).
