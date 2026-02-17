"""IPC Hub main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from logging_utils import setup_logger, generate_trace_id


async def main():
    """Main entry point for IPC Hub."""
    logger = setup_logger("ipc-hub", level="INFO")
    trace_id = generate_trace_id()
    
    logger.info(
        "IPC Hub starting (stub implementation - Phase P1 pending)",
        extra={'trace_id': trace_id}
    )
    
    # TODO: Phase P1-T1 - Implement WebSocket server
    # TODO: Phase P1-T2 - Implement auth handshake
    # TODO: Phase P1-T3 - Implement heartbeat and routing
    # TODO: Phase P1-T4 - Implement schema validation
    
    # Keep service running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("IPC Hub shutting down", extra={'trace_id': trace_id})


if __name__ == "__main__":
    asyncio.run(main())
