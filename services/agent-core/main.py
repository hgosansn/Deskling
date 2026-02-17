"""Agent Core main entry point."""

import asyncio
import sys
from pathlib import Path

# Add shared to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from ipc_client import IPCClient
from logging_utils import generate_trace_id, log_with_trace
from planner import AgentPlanner


# Global state
planner = None
ipc_client = None


async def handle_user_message(msg: dict):
    """Handle chat.user_message from UI."""
    global planner, ipc_client
    
    user_text = msg['payload']['text']
    trace_id = msg['trace_id']
    
    log_with_trace(
        ipc_client.logger, "info",
        f"Received user message: {user_text}",
        trace_id
    )
    
    # Generate plan
    plan_result = planner.analyze_request(user_text)
    
    if plan_result.get('tool_calls'):
        # Send plan with tool proposals
        await ipc_client.send_message(
            to_service="desktop-ui",
            topic="chat.assistant_plan",
            payload={
                "plan_text": plan_result["plan_text"],
                "steps": plan_result["steps"],
                "requires_confirmation": plan_result["requires_confirmation"],
                "tool_calls": plan_result["tool_calls"],
                "confirm_token": generate_trace_id() if plan_result["requires_confirmation"] else None
            },
            trace_id=trace_id,
            reply_to=msg['id']
        )
    else:
        # Simple response without tools
        response_text = plan_result.get("response_text", "I understand.")
        await ipc_client.send_message(
            to_service="desktop-ui",
            topic="chat.assistant_message",
            payload={"text": response_text},
            trace_id=trace_id,
            reply_to=msg['id']
        )


async def handle_confirmation_grant(msg: dict):
    """Handle confirm.grant from UI - execute approved tools."""
    global ipc_client
    
    trace_id = msg['trace_id']
    confirm_token = msg['payload'].get('confirm_token')
    
    log_with_trace(
        ipc_client.logger, "info",
        f"Received confirmation grant: {confirm_token}",
        trace_id
    )
    
    # TODO: Store pending tool calls and retrieve them by confirm_token
    # For now, send a placeholder tool execution
    # In a real implementation, we'd retrieve the tool_calls from a pending dict
    
    await ipc_client.send_message(
        to_service="desktop-ui",
        topic="chat.assistant_message",
        payload={
            "text": "Tools are being executed by automation-service..."
        },
        trace_id=trace_id
    )


async def main():
    """Main entry point for Agent Core."""
    global planner, ipc_client
    
    planner = AgentPlanner()
    ipc_client = IPCClient(
        service_name="agent-core",
        capabilities=["chat.user_message", "chat.assistant_plan", "chat.assistant_message", "confirm.grant"],
        hub_url="ws://127.0.0.1:17171"
    )
    
    # Register message handlers
    ipc_client.register_handler("chat.user_message", handle_user_message)
    ipc_client.register_handler("confirm.grant", handle_confirmation_grant)
    
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
        ipc_client.logger.info("Agent Core shutting down")
        await ipc_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
