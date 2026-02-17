#!/usr/bin/env python3
"""Entry point for IPC hub service."""

from __future__ import annotations

import asyncio

from server import main


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
