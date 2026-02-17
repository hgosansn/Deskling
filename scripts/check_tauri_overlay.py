#!/usr/bin/env python3
"""Verify Tauri overlay window settings required by roadmap task P2-T1."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    cfg_path = Path('apps/desktop-ui/src-tauri/tauri.conf.json')
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))

    windows = (((cfg.get('app') or {}).get('windows')) or [])
    if not windows:
        raise SystemExit('tauri config missing app.windows')

    main_window = windows[0]

    checks = {
        'alwaysOnTop': True,
        'transparent': True,
        'decorations': False
    }

    for key, expected in checks.items():
        got = main_window.get(key)
        if got != expected:
            raise SystemExit(f'overlay check failed: {key} expected {expected!r}, got {got!r}')

    print('overlay config check passed')


if __name__ == '__main__':
    main()
