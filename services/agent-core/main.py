"""Agent Core main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from logging_utils import setup_logger, generate_trace_id


async def main():
    """Main entry point for Agent Core."""
    logger = setup_logger("agent-core", level="INFO")
    trace_id = generate_trace_id()
    
    logger.info(
        "Agent Core starting (stub implementation - Phase P3 pending)",
        extra={'trace_id': trace_id}
    )
    
    # TODO: Phase P3-T1 - Implement agent input/output contract
    # TODO: Phase P3-T2 - Add planner output with risk labeling
    # TODO: Phase P3-T3 - Add tool call proposal format
    # TODO: Phase P3-T4 - Add failure handling
    
    # Keep service running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Agent Core shutting down", extra={'trace_id': trace_id})


if __name__ == "__main__":
    asyncio.run(main())
