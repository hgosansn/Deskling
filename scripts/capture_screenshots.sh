#!/usr/bin/env bash
# Screenshot capture script for PR demos

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCREENSHOT_DIR="$PROJECT_ROOT/demo-screenshots"

echo "📸 Deskling Demo Screenshot Capture"
echo "===================================="

# Create screenshot directory
mkdir -p "$SCREENSHOT_DIR"

# Check for required tools
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -q pillow selenium playwright 2>&1 | grep -v "Requirement already satisfied" || true

# Install playwright browsers
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium 2>&1 | tail -1

# Create virtual environment if needed
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$PROJECT_ROOT/.venv"
fi

source "$PROJECT_ROOT/.venv/bin/activate"

# Install service dependencies
pip install -q -r "$PROJECT_ROOT/shared/requirements.txt" 2>&1 | grep -v "Requirement already satisfied" || true
pip install -q -r "$PROJECT_ROOT/apps/ipc-hub/requirements.txt" 2>&1 | grep -v "Requirement already satisfied" || true
pip install -q -r "$PROJECT_ROOT/services/agent-core/requirements.txt" 2>&1 | grep -v "Requirement already satisfied" || true

echo ""
echo "🚀 Starting services..."

# Start IPC Hub in background
cd "$PROJECT_ROOT/apps/ipc-hub"
python3 -m main &
IPC_HUB_PID=$!
echo "  ✓ IPC Hub started (PID: $IPC_HUB_PID)"

sleep 2

# Start Agent Core in background
cd "$PROJECT_ROOT/services/agent-core"
python3 -m main &
AGENT_CORE_PID=$!
echo "  ✓ Agent Core started (PID: $AGENT_CORE_PID)"

sleep 1

# Run the screenshot capture script
echo ""
echo "📸 Capturing screenshots..."
cd "$PROJECT_ROOT"
python3 scripts/capture_demo.py "$SCREENSHOT_DIR"

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $IPC_HUB_PID $AGENT_CORE_PID 2>/dev/null || true
sleep 1

echo ""
echo "===================================="
echo "✅ Screenshot capture complete!"
echo ""
echo "Screenshots saved to: $SCREENSHOT_DIR"
ls -lh "$SCREENSHOT_DIR"/*.png 2>/dev/null || echo "No screenshots found"
