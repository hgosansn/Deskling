# ipc-hub

Python IPC hub scaffold.

## Current baseline
- Loopback-only WebSocket hub (`server.py`) at `ws://127.0.0.1:17171/ws`
- Minimal envelope validation (`ipc_hub/validation.py`)
- In-memory router for destination queues (`ipc_hub/router.py`)
- Smoke test (`tests/smoke_test.py`)

## Dependency
```bash
pip install -r apps/ipc-hub/requirements.txt
```

## Run smoke test
```bash
PYTHONPATH=apps/ipc-hub python3 apps/ipc-hub/tests/smoke_test.py
```
