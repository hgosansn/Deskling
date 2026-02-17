"""WebSocket server implementation for IPC Hub."""

import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
from typing import Dict, Set, Optional
from datetime import datetime, timezone
import jsonschema
from pathlib import Path

from logging_utils import setup_logger, generate_trace_id, log_with_trace


class IPCHub:
    """WebSocket-based IPC message router."""

    def __init__(self, host: str = "127.0.0.1", port: int = 17171):
        self.host = host
        self.port = port
        self.logger = setup_logger("ipc-hub", level="INFO")
        
        # Connected services
        self.services: Dict[str, WebSocketServerProtocol] = {}
        self.service_capabilities: Dict[str, list] = {}
        
        # Load schemas
        schemas_dir = Path(__file__).parent.parent.parent / "shared" / "schemas"
        with open(schemas_dir / "envelope.json") as f:
            self.envelope_schema = json.load(f)
        with open(schemas_dir / "auth_topics.json") as f:
            self.auth_schemas = json.load(f)
        
        self.logger.info(f"IPC Hub initialized on {host}:{port}")

    async def start(self):
        """Start the WebSocket server."""
        trace_id = generate_trace_id()
        log_with_trace(
            self.logger, "info",
            f"Starting IPC Hub on {self.host}:{self.port}",
            trace_id
        )
        
        async with websockets.serve(
            self.handle_connection,
            self.host,
            self.port,
            ping_interval=30,
            ping_timeout=10
        ):
            log_with_trace(
                self.logger, "info",
                f"IPC Hub listening on ws://{self.host}:{self.port}/ws",
                trace_id
            )
            await asyncio.Future()  # Run forever

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        """Handle a new WebSocket connection."""
        trace_id = generate_trace_id()
        client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        
        log_with_trace(
            self.logger, "info",
            f"New connection from {client_addr}",
            trace_id
        )
        
        service_name = None
        
        try:
            # Wait for auth.hello message
            auth_result = await self.authenticate(websocket, trace_id)
            if not auth_result:
                return
            
            service_name = auth_result["service_name"]
            
            # Keep connection alive and route messages
            await self.message_loop(websocket, service_name, trace_id)
            
        except websockets.exceptions.ConnectionClosed:
            log_with_trace(
                self.logger, "info",
                f"Connection closed for {service_name or client_addr}",
                trace_id
            )
        except Exception as e:
            log_with_trace(
                self.logger, "error",
                f"Error handling connection: {e}",
                trace_id
            )
        finally:
            # Cleanup
            if service_name and service_name in self.services:
                del self.services[service_name]
                del self.service_capabilities[service_name]
                log_with_trace(
                    self.logger, "info",
                    f"Service {service_name} disconnected and removed",
                    trace_id
                )

    async def authenticate(
        self,
        websocket: WebSocketServerProtocol,
        trace_id: str
    ) -> Optional[dict]:
        """
        Authenticate a new connection.
        
        Returns service info dict if successful, None otherwise.
        """
        try:
            # Wait for first message (timeout 10 seconds)
            raw_msg = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            msg = json.loads(raw_msg)
            
            # Validate envelope
            jsonschema.validate(instance=msg, schema=self.envelope_schema)
            
            # Check topic is auth.hello
            if msg["topic"] != "auth.hello":
                await self.send_auth_error(
                    websocket,
                    "INVALID_SERVICE",
                    "First message must be auth.hello",
                    trace_id
                )
                return None
            
            # Validate auth.hello payload
            payload = msg["payload"]
            jsonschema.validate(
                instance=payload,
                schema=self.auth_schemas["definitions"]["auth_hello"]
            )
            
            service_name = payload["service_name"]
            
            # Check if service already registered
            if service_name in self.services:
                await self.send_auth_error(
                    websocket,
                    "DUPLICATE_SERVICE",
                    f"Service {service_name} already connected",
                    trace_id
                )
                return None
            
            # Register service
            self.services[service_name] = websocket
            self.service_capabilities[service_name] = payload.get("capabilities", [])
            
            # Send auth.ok
            response = self.create_message(
                from_service="ipc-hub",
                to_service=service_name,
                topic="auth.ok",
                payload={
                    "session_token": generate_trace_id(),  # Simple token for now
                    "expires_at": datetime.now(timezone.utc).isoformat()
                },
                trace_id=trace_id,
                reply_to=msg["id"]
            )
            await websocket.send(json.dumps(response))
            
            log_with_trace(
                self.logger, "info",
                f"Service {service_name} authenticated with capabilities: {payload.get('capabilities', [])}",
                trace_id
            )
            
            return payload
            
        except asyncio.TimeoutError:
            log_with_trace(
                self.logger, "warning",
                "Authentication timeout",
                trace_id
            )
            return None
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            log_with_trace(
                self.logger, "error",
                f"Invalid auth message: {e}",
                trace_id
            )
            await self.send_auth_error(
                websocket,
                "AUTH_FAILED",
                str(e),
                trace_id
            )
            return None

    async def send_auth_error(
        self,
        websocket: WebSocketServerProtocol,
        code: str,
        message: str,
        trace_id: str
    ):
        """Send an auth error response."""
        response = self.create_message(
            from_service="ipc-hub",
            to_service="unknown",
            topic="auth.error",
            payload={"code": code, "message": message},
            trace_id=trace_id
        )
        await websocket.send(json.dumps(response))
        await websocket.close()

    async def message_loop(
        self,
        websocket: WebSocketServerProtocol,
        service_name: str,
        trace_id: str
    ):
        """Main message routing loop for authenticated service."""
        async for raw_msg in websocket:
            try:
                msg = json.loads(raw_msg)
                
                # Validate envelope
                jsonschema.validate(instance=msg, schema=self.envelope_schema)
                
                # Extract routing info
                to_service = msg["to"]
                topic = msg["topic"]
                msg_trace_id = msg["trace_id"]
                
                log_with_trace(
                    self.logger, "debug",
                    f"Routing {topic} from {service_name} to {to_service}",
                    msg_trace_id
                )
                
                # Handle heartbeat locally
                if topic == "hb.ping":
                    response = self.create_message(
                        from_service="ipc-hub",
                        to_service=service_name,
                        topic="hb.pong",
                        payload={},
                        trace_id=msg_trace_id,
                        reply_to=msg["id"]
                    )
                    await websocket.send(json.dumps(response))
                    continue
                
                # Route to target service
                if to_service == "broadcast":
                    # Broadcast to all except sender
                    for target_name, target_ws in self.services.items():
                        if target_name != service_name:
                            await target_ws.send(raw_msg)
                elif to_service in self.services:
                    # Send to specific service
                    await self.services[to_service].send(raw_msg)
                else:
                    # Service not found
                    log_with_trace(
                        self.logger, "warning",
                        f"Target service {to_service} not connected",
                        msg_trace_id
                    )
                    
            except json.JSONDecodeError as e:
                log_with_trace(
                    self.logger, "error",
                    f"Invalid JSON from {service_name}: {e}",
                    trace_id
                )
            except jsonschema.ValidationError as e:
                log_with_trace(
                    self.logger, "error",
                    f"Schema validation failed from {service_name}: {e}",
                    trace_id
                )

    def create_message(
        self,
        from_service: str,
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
            "from": from_service,
            "to": to_service,
            "topic": topic,
            "reply_to": reply_to,
            "trace_id": trace_id,
            "payload": payload
        }
