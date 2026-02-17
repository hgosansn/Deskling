"""Skin-pack manifest loader/validator for P6 baseline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ManifestError(Exception):
    code: str
    message: str


REQUIRED_KEYS = {'id', 'name', 'version', 'assets'}
REQUIRED_ASSETS = {'idle', 'talk', 'emotion'}


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_KEYS - set(manifest.keys())
    if missing:
        raise ManifestError('ERR_MANIFEST_KEYS', f'missing keys: {sorted(missing)}')

    for key in ('id', 'name', 'version'):
        value = manifest.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ManifestError('ERR_MANIFEST_FIELD', f'{key} must be non-empty string')

    assets = manifest.get('assets')
    if not isinstance(assets, dict):
        raise ManifestError('ERR_MANIFEST_ASSETS', 'assets must be an object')

    missing_assets = REQUIRED_ASSETS - set(assets.keys())
    if missing_assets:
        raise ManifestError('ERR_MANIFEST_ASSETS', f'missing assets: {sorted(missing_assets)}')

    for key in REQUIRED_ASSETS:
        val = assets.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ManifestError('ERR_MANIFEST_ASSETS', f'asset {key} must be non-empty string path')

    return manifest


def load_manifest(path: str | Path) -> dict[str, Any]:
    src = Path(path)
    if not src.exists():
        raise ManifestError('ERR_MANIFEST_NOT_FOUND', f'manifest not found: {src}')

    try:
        data = json.loads(src.read_text(encoding='utf-8'))
    except json.JSONDecodeError as err:
        raise ManifestError('ERR_MANIFEST_JSON', f'invalid json: {err}') from err

    if not isinstance(data, dict):
        raise ManifestError('ERR_MANIFEST_TYPE', 'manifest root must be object')

    return validate_manifest(data)
