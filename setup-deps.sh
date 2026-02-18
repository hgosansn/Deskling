#!/bin/bash
# Deskling Setup Script
# Installs system dependencies for building Tauri applications

set -e

echo "🔧 Deskling Setup - Installing System Dependencies"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Detect Linux distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    else
        echo "❌ Cannot detect Linux distribution"
        exit 1
    fi

    case $OS in
        ubuntu|debian|pop|linuxmint)
            echo "📦 Detected Ubuntu/Debian-based distribution"
            echo "Installing dependencies..."
            sudo apt-get update
            sudo apt-get install -y \
              pkg-config \
              libglib2.0-dev \
              libgtk-3-dev \
              libwebkit2gtk-4.1-dev \
              libappindicator3-dev \
              librsvg2-dev \
              patchelf \
              build-essential
            ;;
        fedora|rhel|centos)
            echo "📦 Detected Fedora/RHEL-based distribution"
            echo "Installing dependencies..."
            sudo dnf install -y \
              pkg-config \
              glib2-devel \
              gtk3-devel \
              webkit2gtk4.1-devel \
              libappindicator-gtk3-devel \
              librsvg2-devel \
              patchelf \
              gcc-c++
            ;;
        arch|manjaro)
            echo "📦 Detected Arch-based distribution"
            echo "Installing dependencies..."
            sudo pacman -S --needed \
              pkg-config \
              glib2 \
              gtk3 \
              webkit2gtk-4.1 \
              libappindicator-gtk3 \
              librsvg \
              patchelf \
              base-devel
            ;;
        *)
            echo "❌ Unsupported Linux distribution: $OS"
            echo "Please install dependencies manually. See README.md"
            exit 1
            ;;
    esac

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Detected macOS"
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install 2>/dev/null || echo "Xcode Command Line Tools already installed"

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "📦 Detected Windows"
    echo "Please install Visual Studio Build Tools from:"
    echo "https://visualstudio.microsoft.com/downloads/"
    exit 0

else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo ""
echo "✅ System dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "  1. Install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
echo "  2. Install Tauri CLI: cargo install tauri-cli"
echo "  3. Build the app: cd apps/desktop-ui/src-tauri && cargo tauri dev"
echo ""
