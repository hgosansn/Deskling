#!/usr/bin/env python3
"""Stub automation-service process used for logging convention rollout."""

from __future__ import annotations

import logging
import time

from tasksprite_common import get_service_logger, new_trace_id
from tools import LowRiskToolExecutor


def main() -> None:
    logger = get_service_logger('automation-service')
    executor = LowRiskToolExecutor()
    logger.event(
        logging.INFO,
        'service.start',
        new_trace_id(),
        mode='low-risk-tools-v0',
        tools=[
            'clipboard.read',
            'clipboard.write',
            'notify.send',
            'apps.open',
            'browser.open_url',
            'files.list_dir',
            'files.read_text',
            'files.write_text'
        ]
    )

    try:
        while True:
            _ = executor
            logger.event(logging.INFO, 'policy.ready', new_trace_id(), profile='default')
            time.sleep(5)
    except KeyboardInterrupt:
        logger.event(logging.INFO, 'service.stop', new_trace_id(), reason='interrupt')


if __name__ == '__main__':
    main()
