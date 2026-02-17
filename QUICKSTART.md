# Deskling Quick Start Guide

## Prerequisites

- Python 3.10+ 
- Node.js 16+ (for Electron UI)
- pip and npm

## Setup (First Time)

### 1. Clone and Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install shared dependencies
pip install -r shared/requirements.txt

# Install service dependencies
pip install -r apps/ipc-hub/requirements.txt
pip install -r services/agent-core/requirements.txt
pip install -r services/automation-service/requirements.txt
```

### 2. Install Desktop UI Dependencies

```bash
cd apps/desktop-ui
npm install
cd ../..
```

## Running the System

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - IPC Hub:**
```bash
source .venv/bin/activate
cd apps/ipc-hub
python3 -m main
```

**Terminal 2 - Agent Core:**
```bash
source .venv/bin/activate
cd services/agent-core
python3 -m main
```

**Terminal 3 - Automation Service:**
```bash
source .venv/bin/activate
cd services/automation-service
python3 -m main
```

**Terminal 4 - Desktop UI:**
```bash
cd apps/desktop-ui
npm start
# Or for dev mode with DevTools:
npm run dev
```

### Option 2: Script Start (All Python Services)

```bash
./scripts/dev-up.sh
```

Then in a separate terminal:
```bash
cd apps/desktop-ui
npm start
```

## Using Deskling

1. **Desktop UI will appear** - A semi-transparent overlay window
2. **Type a message** in the input box at the bottom
3. **Try these commands**:
   - "Hello" - Simple greeting
   - "Send me a notification" - Triggers notify.send tool
   - "Copy this text to clipboard" - Triggers clipboard.write
   - "Open https://github.com" - Opens URL in browser
   - "Help" - Lists available capabilities

4. **Watch the state indicator** - Colored dot in header shows current state:
   - Green (idle) - Ready for input
   - Yellow (thinking) - Processing request
   - Blue (speaking) - Would be speaking (voice pending P5)
   - Orange (running) - Executing tools
   - Red (error) - Error state

5. **For tool proposals requiring confirmation**:
   - Plan will be displayed with risk-colored steps
   - Green = low risk, Yellow = medium, Red = high
   - Click "Approve" to execute or "Deny" to cancel

## Architecture at a Glance

```
Desktop UI (Electron)
    ↕ WebSocket
IPC Hub (127.0.0.1:17171)
    ↕
Agent Core ← Plans user requests
Automation Service ← Executes tools
```

## Logs

All services log to console with trace IDs for request correlation.

Example log format:
```
2026-02-17 12:00:00 | agent-core | INFO | trace_id=01HQXYZ... | Received user message: Hello
```

## Troubleshooting

**Connection refused errors?**
- Make sure IPC Hub is running first
- Check that it's bound to 127.0.0.1:17171

**Electron window doesn't appear?**
- Check console for errors
- Try `npm run dev` for DevTools access

**Tools not executing?**
- Verify automation-service is connected (check IPC Hub logs)
- Check automation-service logs for errors

**Path permission errors on file operations?**
- By default only ~/Documents and ~/Downloads are allowed
- Edit `configs/default.toml` to add more paths

## Configuration

Edit `configs/default.toml` to customize:
- IPC host/port
- Model provider (when LLM integration is added)
- Allowed file paths
- Log level

Edit `configs/permissions.toml` to customize:
- Tool risk levels
- Confirmation requirements

## Development Tips

1. **Run with DevTools**: `npm run dev` in desktop-ui for debugging
2. **View trace IDs**: All messages include trace_id for end-to-end tracking
3. **Check audit log**: Automation service maintains audit log of all tool executions
4. **Test IPC**: Use `./scripts/test_ipc.py` to test IPC Hub connectivity

## Next Steps

- **Phase P5**: Voice integration (STT/TTS) - in progress
- **Phase P6**: Character skins - planned
- **Phase P7**: Installers and hardening - planned

See `ROADMAP.md` for full project plan.

## Getting Help

- Read `IMPLEMENTATION_SUMMARY.md` for architecture details
- Check `specs/` folder for design documents
- Review service READMEs in each service directory

---

Happy assisting! 🚀
