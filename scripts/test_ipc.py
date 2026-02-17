#!/usr/bin/env python3
"""Test script for IPC Hub and Client."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))

from ipc_client import IPCClient


async def test_client():
    """Test IPC client connection."""
    client = IPCClient(
        service_name="test-service",
        capabilities=["test.echo"],
        hub_url="ws://127.0.0.1:17171"
    )
    
    try:
        print("🧪 Connecting to IPC Hub...")
        await client.connect()
        print("✅ Connected and authenticated!")
        
        # Send a test message
        print("📤 Sending test message...")
        await client.send_message(
            to_service="agent-core",
            topic="chat.user_message",
            payload={"text": "Hello from test script!"}
        )
        print("✅ Message sent!")
        
        # Wait a bit then disconnect
        await asyncio.sleep(2)
        
        await client.disconnect()
        print("✅ Test complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_client())
    sys.exit(exit_code)
