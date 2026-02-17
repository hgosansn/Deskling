"""WebSocket client for connecting to IPC Hub."""

import asyncio
import json
import os
import websockets
from typing import Callable, Optional, Dict
from datetime import datetime, timezone
import jsonschema
from pathlib import Path

from logging_utils import setup_logger, generate_trace_id, log_with_trace


class IPCClient:
    """WebSocket client for IPC Hub communication."""

    def __init__(
        self,
        service_name: str,
        capabilities: list,
        hub_url: str = "ws://127.0.0.1:17171/ws",
        version: str = "0.1.0"
    ):
        self.service_name = service_name
        self.capabilities = capabilities
        self.hub_url = hub_url
        self.version = version
        self.logger = setup_logger(service_name, level="INFO")
        
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.authenticated = False
        self.session_token: Optional[str] = None
        
        # Message handlers by topic
        self.handlers: Dict[str, Callable] = {}
        
        # Load envelope schema for validation
        schemas_dir = Path(__file__).parent / "schemas"
        if schemas_dir.exists():
            with open(schemas_dir / "envelope.json") as f:
                self.envelope_schema = json.load(f)
        else:
            self.envelope_schema = None
        
    def register_handler(self, topic: str, handler: Callable):
        """Register a handler for a specific topic."""
        self.handlers[topic] = handler
        self.logger.debug(f"Registered handler for topic: {topic}")

    async def connect(self):
        """Connect to IPC Hub and authenticate."""
        trace_id = generate_trace_id()
        
        try:
            log_with_trace(
                self.logger, "info",
                f"Connecting to IPC Hub at {self.hub_url}",
                trace_id
            )
            
            self.websocket = await websockets.connect(self.hub_url)
            
            # Send auth.hello
            auth_msg = self.create_message(
                to_service="ipc-hub",
                topic="auth.hello",
                payload={
                    "service": self.service_name,
                    "service_name": self.service_name,
                    "capabilities": self.capabilities,
                    "version": self.version,
                    "token": os.getenv("TASKSPRITE_IPC_TOKEN", "dev-token")
                },
                trace_id=trace_id
            )
            
            await self.websocket.send(json.dumps(auth_msg))
            
            # Wait for auth.ok
            response_raw = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            response = json.loads(response_raw)
            
            if response["topic"] == "auth.ok":
                self.session_token = (response.get("payload") or {}).get("session_token")
                self.authenticated = True
                log_with_trace(
                    self.logger, "info",
                    f"Successfully authenticated to IPC Hub",
                    trace_id
                )
            elif response["topic"] == "auth.error":
                error_msg = response["payload"]["message"]
                log_with_trace(
                    self.logger, "error",
                    f"Authentication failed: {error_msg}",
                    trace_id
                )
                raise ConnectionError(f"Authentication failed: {error_msg}")
            
        except Exception as e:
            log_with_trace(
                self.logger, "error",
                f"Failed to connect to IPC Hub: {e}",
                trace_id
            )
            raise

    async def send_message(
        self,
        to_service: str,
        topic: str,
        payload: dict,
        trace_id: Optional[str] = None,
        reply_to: Optional[str] = None
    ):
        """Send a message to another service via IPC Hub."""
        if not self.authenticated:
            raise RuntimeError("Not authenticated to IPC Hub")
        
        if trace_id is None:
            trace_id = generate_trace_id()
        
        msg = self.create_message(
            to_service=to_service,
            topic=topic,
            payload=payload,
            trace_id=trace_id,
            reply_to=reply_to
        )
        
        await self.websocket.send(json.dumps(msg))
        
        log_with_trace(
            self.logger, "debug",
            f"Sent {topic} to {to_service}",
            trace_id
        )

    async def message_loop(self):
        """Main message receive loop."""
        trace_id = generate_trace_id()
        
        log_with_trace(
            self.logger, "info",
            "Starting message loop",
            trace_id
        )
        
        try:
            async for raw_msg in self.websocket:
                msg = json.loads(raw_msg)
                topic = msg["topic"]
                msg_trace_id = msg["trace_id"]
                
                # Handle heartbeat pong
                if topic == "hb.pong":
                    log_with_trace(
                        self.logger, "debug",
                        "Received heartbeat pong",
                        msg_trace_id
                    )
                    continue
                
                # Dispatch to registered handler
                if topic in self.handlers:
                    try:
                        await self.handlers[topic](msg)
                    except Exception as e:
                        log_with_trace(
                            self.logger, "error",
                            f"Error in handler for {topic}: {e}",
                            msg_trace_id
                        )
                else:
                    log_with_trace(
                        self.logger, "warning",
                        f"No handler registered for topic: {topic}",
                        msg_trace_id
                    )
                    
        except websockets.exceptions.ConnectionClosed:
            log_with_trace(
                self.logger, "warning",
                "Connection to IPC Hub closed",
                trace_id
            )
            self.authenticated = False

    async def send_heartbeat(self):
        """Send periodic heartbeat to IPC Hub."""
        while self.authenticated:
            try:
                await self.send_message(
                    to_service="ipc-hub",
                    topic="hb.ping",
                    payload={}
                )
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Heartbeat failed: {e}")
                break

    def create_message(
        self,
        to_service: str,
        topic: str,
        payload: dict,
        trace_id: str,
        reply_to: Optional[str] = None
    ) -> dict:
        """Create a properly formatted IPC message."""
        return {
            "v": 1,
            "id": generate_trace_id(),
            "ts": datetime.now(timezone.utc).isoformat(),
            "from": self.service_name,
            "to": to_service,
            "topic": topic,
            "reply_to": reply_to,
            "trace_id": trace_id,
            "payload": payload
        }

    async def disconnect(self):
        """Disconnect from IPC Hub."""
        if self.websocket:
            await self.websocket.close()
            self.authenticated = False
            self.logger.info("Disconnected from IPC Hub")
