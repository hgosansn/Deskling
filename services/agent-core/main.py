"""Agent Core main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from ipc_client import IPCClient
from logging_utils import generate_trace_id, log_with_trace


async def handle_user_message(msg: dict):
    """Handle chat.user_message from UI."""
    # TODO: Phase P3 - Implement actual planning and tool proposal
    # For now, just echo back
    print(f"Received user message: {msg['payload']['text']}")


async def main():
    """Main entry point for Agent Core."""
    client = IPCClient(
        service_name="agent-core",
        capabilities=["chat.user_message", "chat.assistant_plan", "chat.assistant_message"],
        hub_url="ws://127.0.0.1:17171"
    )
    
    # Register message handlers
    client.register_handler("chat.user_message", handle_user_message)
    
    try:
        # Connect to IPC Hub
        await client.connect()
        
        # Start heartbeat
        heartbeat_task = asyncio.create_task(client.send_heartbeat())
        
        # Start message loop
        await client.message_loop()
        
        # Cleanup
        heartbeat_task.cancel()
        await client.disconnect()
        
    except KeyboardInterrupt:
        client.logger.info("Agent Core shutting down")
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
