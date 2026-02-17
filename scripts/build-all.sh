#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHONPATH_ROOT="$ROOT_DIR/shared/python:$ROOT_DIR/apps/ipc-hub:$ROOT_DIR/services/agent-core"

cd "$ROOT_DIR"

echo "[build-all] frontend build"
npm run build

echo "[build-all] desktop-ui state machine tests"
node "$ROOT_DIR/apps/desktop-ui/src/state_machine.test.mjs"

echo "[build-all] desktop-ui confirm policy tests"
node "$ROOT_DIR/apps/desktop-ui/src/confirm_policy.test.mjs"

echo "[build-all] desktop-ui settings store tests"
node "$ROOT_DIR/apps/desktop-ui/src/settings_store.test.mjs"

echo "[build-all] desktop-ui skin tests"
node "$ROOT_DIR/apps/desktop-ui/src/skins.test.mjs"

echo "[build-all] desktop-ui syntax checks"
node --check "$ROOT_DIR/apps/desktop-ui/src/main.js"

echo "[build-all] shared schema checks"
python3 "$ROOT_DIR/scripts/check_schemas.py"

echo "[build-all] tauri overlay config check"
python3 "$ROOT_DIR/scripts/check_tauri_overlay.py"

echo "[build-all] tauri rust host check"
cargo check --manifest-path "$ROOT_DIR/apps/desktop-ui/src-tauri/Cargo.toml"

echo "[build-all] python service syntax check"
for svc in \
    "$ROOT_DIR/apps/ipc-hub/ipc_hub/validation.py" \
    "$ROOT_DIR/apps/ipc-hub/ipc_hub/router.py" \
    "$ROOT_DIR/apps/ipc-hub/server.py" \
    "$ROOT_DIR/apps/ipc-hub/main.py" \
    "$ROOT_DIR/apps/ipc-hub/tests/smoke_test.py" \
    "$ROOT_DIR/apps/ipc-hub/tests/test_validation.py" \
    "$ROOT_DIR/apps/ipc-hub/tests/test_router.py" \
    "$ROOT_DIR/apps/ipc-hub/tests/test_server.py" \
    "$ROOT_DIR/services/agent-core/contract.py" \
    "$ROOT_DIR/services/agent-core/failure_templates.py" \
    "$ROOT_DIR/services/agent-core/planner.py" \
    "$ROOT_DIR/services/agent-core/main.py" \
    "$ROOT_DIR/services/agent-core/tests/test_contract.py" \
    "$ROOT_DIR/services/agent-core/tests/test_agent_core.py" \
    "$ROOT_DIR/services/agent-core/tests/test_failure_templates.py" \
    "$ROOT_DIR/services/agent-core/tests/test_planner.py" \
    "$ROOT_DIR/services/automation-service/tools.py" \
    "$ROOT_DIR/services/automation-service/main.py" \
    "$ROOT_DIR/services/automation-service/tests/test_tools.py" \
    "$ROOT_DIR/services/voice-service/capture.py" \
    "$ROOT_DIR/services/voice-service/playback.py" \
    "$ROOT_DIR/services/voice-service/stt_adapter.py" \
    "$ROOT_DIR/services/voice-service/tts_adapter.py" \
    "$ROOT_DIR/services/voice-service/main.py" \
    "$ROOT_DIR/services/voice-service/tests/test_capture.py" \
    "$ROOT_DIR/services/voice-service/tests/test_playback.py" \
    "$ROOT_DIR/services/voice-service/tests/test_stt_adapter.py" \
    "$ROOT_DIR/services/voice-service/tests/test_tts_adapter.py" \
    "$ROOT_DIR/services/skin-service/manifest.py" \
    "$ROOT_DIR/services/skin-service/tests/test_manifest.py" \
    "$ROOT_DIR/services/skin-service/main.py"; do
    PYTHONPATH="$PYTHONPATH_ROOT" python3 -m py_compile "$svc"
done

echo "[build-all] ipc-hub routing smoke test"
PYTHONPATH="$ROOT_DIR/apps/ipc-hub" python3 "$ROOT_DIR/apps/ipc-hub/tests/smoke_test.py"

echo "[build-all] ipc-hub unit tests"
PYTHONPATH="$PYTHONPATH_ROOT" python3 -m unittest discover -s "$ROOT_DIR/apps/ipc-hub/tests" -p "test_*.py"

echo "[build-all] agent-core unit tests"
PYTHONPATH="$PYTHONPATH_ROOT" python3 -m unittest discover -s "$ROOT_DIR/services/agent-core/tests" -p "test_*.py"

echo "[build-all] automation-service unit tests"
PYTHONPATH="$PYTHONPATH_ROOT" python3 -m unittest discover -s "$ROOT_DIR/services/automation-service/tests" -p "test_*.py"

echo "[build-all] voice-service unit tests"
PYTHONPATH="$PYTHONPATH_ROOT" python3 -m unittest discover -s "$ROOT_DIR/services/voice-service/tests" -p "test_*.py"

echo "[build-all] skin-service unit tests"
PYTHONPATH="$PYTHONPATH_ROOT" python3 -m unittest discover -s "$ROOT_DIR/services/skin-service/tests" -p "test_*.py"

echo "[build-all] complete"
