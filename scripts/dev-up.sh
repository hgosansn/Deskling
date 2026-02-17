#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs/dev"
PYTHONPATH_ROOT="$ROOT_DIR/shared/python:$ROOT_DIR/apps/ipc-hub"

mkdir -p "$LOG_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required" >&2
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required" >&2
    exit 1
fi

pids=()

cleanup() {
    for pid in "${pids[@]:-}"; do
        if kill -0 "$pid" >/dev/null 2>&1; then
            kill "$pid" >/dev/null 2>&1 || true
        fi
    done
}
trap cleanup EXIT INT TERM

start_process() {
    local name="$1"
    shift

    echo "[dev-up] starting $name"
    "$@" >"$LOG_DIR/$name.log" 2>&1 &
    pids+=("$!")
}

start_process "ipc-hub" env PYTHONPATH="$PYTHONPATH_ROOT" python3 "$ROOT_DIR/apps/ipc-hub/main.py"
start_process "agent-core" env PYTHONPATH="$PYTHONPATH_ROOT" python3 "$ROOT_DIR/services/agent-core/main.py"
start_process "desktop-ui" npm run dev

echo "[dev-up] running services. logs: $LOG_DIR"
wait -n "${pids[@]}"
