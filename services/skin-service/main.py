#!/usr/bin/env python3
"""Stub skin-service process used for logging convention rollout."""

from __future__ import annotations

import logging
import time

from manifest import load_manifest
from tasksprite_common import get_service_logger, new_trace_id


def main() -> None:
    logger = get_service_logger('skin-service')
    manifest = load_manifest('shared/skins/default_skin/manifest.json')
    logger.event(logging.INFO, 'service.start', new_trace_id(), mode='skin-pack-v0', default_skin=manifest['id'])

    try:
        while True:
            logger.event(logging.INFO, 'skin.catalog.ready', new_trace_id(), skin_count=1)
            time.sleep(5)
    except KeyboardInterrupt:
        logger.event(logging.INFO, 'service.stop', new_trace_id(), reason='interrupt')


if __name__ == '__main__':
    main()
