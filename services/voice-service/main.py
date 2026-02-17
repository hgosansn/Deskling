"""Voice Service main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from logging_utils import setup_logger, generate_trace_id


async def main():
    """Main entry point for Voice Service."""
    logger = setup_logger("voice-service", level="INFO")
    trace_id = generate_trace_id()
    
    logger.info(
        "Voice Service starting (stub implementation - Phase P5 pending)",
        extra={'trace_id': trace_id}
    )
    
    # TODO: Phase P5-T1 - Implement push-to-talk capture
    # TODO: Phase P5-T2 - Integrate STT adapter
    # TODO: Phase P5-T3 - Integrate Piper TTS
    # TODO: Phase P5-T4 - Add barge-in
    
    # Keep service running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Voice Service shutting down", extra={'trace_id': trace_id})


if __name__ == "__main__":
    asyncio.run(main())
