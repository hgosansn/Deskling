"""IPC Hub main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from server import IPCHub


async def main():
    """Main entry point for IPC Hub."""
    hub = IPCHub(host="127.0.0.1", port=17171)
    
    try:
        await hub.start()
    except KeyboardInterrupt:
        hub.logger.info("IPC Hub shutting down")


if __name__ == "__main__":
    asyncio.run(main())
