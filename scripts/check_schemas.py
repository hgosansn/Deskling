#!/usr/bin/env python3
"""Basic validation for JSON schema files committed under shared/schemas."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path('shared/schemas')
    files = sorted(root.rglob('*.json'))
    if not files:
        raise SystemExit('no schema files found under shared/schemas')

    for path in files:
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('type') != 'object':
            raise SystemExit(f'{path}: schema type must be object')
        if 'properties' not in data:
            raise SystemExit(f'{path}: missing properties')
        if 'required' not in data:
            raise SystemExit(f'{path}: missing required list')

    print(f'schema checks passed ({len(files)} files)')


if __name__ == '__main__':
    main()
