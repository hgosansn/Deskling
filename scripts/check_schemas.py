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
        # Accept either:
        # 1) a direct object schema with properties/required, or
        # 2) a schema container with definitions of object payload schemas.
        if data.get('type') == 'object':
            if 'properties' not in data:
                raise SystemExit(f'{path}: missing properties')
            if 'required' not in data:
                raise SystemExit(f'{path}: missing required list')
            continue

        definitions = data.get('definitions')
        if not isinstance(definitions, dict) or not definitions:
            raise SystemExit(f'{path}: unsupported schema shape (expected object schema or non-empty definitions)')

        for name, schema in definitions.items():
            if not isinstance(schema, dict):
                raise SystemExit(f'{path}: definition {name} must be an object')
            if schema.get('type') != 'object':
                raise SystemExit(f'{path}: definition {name} type must be object')
            if 'properties' not in schema:
                raise SystemExit(f'{path}: definition {name} missing properties')
            if 'required' not in schema:
                raise SystemExit(f'{path}: definition {name} missing required list')

    print(f'schema checks passed ({len(files)} files)')


if __name__ == '__main__':
    main()
