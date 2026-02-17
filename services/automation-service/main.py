"""Automation Service main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from ipc_client import IPCClient
from logging_utils import generate_trace_id, log_with_trace
from tools import ToolExecutor


# Global state
tool_executor = None
ipc_client = None


async def handle_tool_execute(msg: dict):
    """Handle tool.execute from agent-core."""
    global tool_executor, ipc_client
    
    trace_id = msg['trace_id']
    payload = msg['payload']
    
    tool_name = payload.get('tool')
    args = payload.get('args', {})
    confirm_token = payload.get('confirm_token')
    
    log_with_trace(
        ipc_client.logger, "info",
        f"Executing tool: {tool_name}",
        trace_id
    )
    
    # TODO: Phase P4-T3 - Validate confirm_token if required
    # For now, execute directly
    
    result = tool_executor.execute_tool(tool_name, args, trace_id)
    
    # Send result back
    await ipc_client.send_message(
        to_service=msg['from'],
        topic="tool.results",
        payload={
            "success": result["success"],
            "result": result.get("result"),
            "error": result.get("error"),
            "audit_id": result["audit_info"]["timestamp"]
        },
        trace_id=trace_id,
        reply_to=msg['id']
    )
    
    if result["success"]:
        log_with_trace(
            ipc_client.logger, "info",
            f"Tool {tool_name} executed successfully",
            trace_id
        )
    else:
        log_with_trace(
            ipc_client.logger, "error",
            f"Tool {tool_name} failed: {result['error']}",
            trace_id
        )


async def main():
    """Main entry point for Automation Service."""
    global tool_executor, ipc_client
    
    tool_executor = ToolExecutor()
    ipc_client = IPCClient(
        service_name="automation-service",
        capabilities=["tool.execute", "tool.results"],
        hub_url="ws://127.0.0.1:17171"
    )
    
    # Register message handlers
    ipc_client.register_handler("tool.execute", handle_tool_execute)
    
    try:
        # Connect to IPC Hub
        await ipc_client.connect()
        
        # Start heartbeat
        heartbeat_task = asyncio.create_task(ipc_client.send_heartbeat())
        
        # Start message loop
        await ipc_client.message_loop()
        
        # Cleanup
        heartbeat_task.cancel()
        await ipc_client.disconnect()
        
    except KeyboardInterrupt:
        ipc_client.logger.info("Automation Service shutting down")
        await ipc_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
