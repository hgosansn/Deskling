#!/usr/bin/env bash
# Development startup script - starts all services

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 Starting Deskling Voice Desktop Mate (Development Mode)"
echo "================================================"

# Check for Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$PROJECT_ROOT/.venv"
fi

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Install dependencies for all services
echo ""
echo "📦 Installing Python dependencies..."
pip install -q -r "$PROJECT_ROOT/shared/requirements.txt"
pip install -q -r "$PROJECT_ROOT/apps/ipc-hub/requirements.txt"
pip install -q -r "$PROJECT_ROOT/services/agent-core/requirements.txt"
pip install -q -r "$PROJECT_ROOT/services/automation-service/requirements.txt"
pip install -q -r "$PROJECT_ROOT/services/voice-service/requirements.txt"

echo "✓ Dependencies installed"
echo ""

# Create log directory
mkdir -p "$HOME/.deskling/logs"

# Start services in background
echo "🔧 Starting services..."

# Start IPC Hub
echo "  Starting ipc-hub on 127.0.0.1:17171..."
cd "$PROJECT_ROOT/apps/ipc-hub"
python3 -m main &
IPC_HUB_PID=$!
echo "  ✓ ipc-hub (PID: $IPC_HUB_PID)"

sleep 2

# Start Agent Core (stub)
echo "  Starting agent-core..."
cd "$PROJECT_ROOT/services/agent-core"
python3 -m main &
AGENT_CORE_PID=$!
echo "  ✓ agent-core (PID: $AGENT_CORE_PID)"

sleep 1

# Start Desktop UI (if Electron is set up, otherwise just notify)
echo "  Desktop UI setup pending (Phase P2)"

echo ""
echo "================================================"
echo "✅ Development environment is running!"
echo ""
echo "Services:"
echo "  - IPC Hub:    ws://127.0.0.1:17171/ws"
echo "  - Agent Core: Connected"
echo ""
echo "Logs: $HOME/.deskling/logs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C and cleanup
trap "echo 'Stopping services...'; kill $IPC_HUB_PID $AGENT_CORE_PID 2>/dev/null; exit 0" INT TERM

# Wait for background processes
wait
