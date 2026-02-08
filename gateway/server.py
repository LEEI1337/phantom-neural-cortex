"""
Gateway Server

WebSocket gateway server on port 18789 (OpenClaw-inspired).
Centralized control plane for message routing and session management.
"""

import asyncio
import logging
import socketio
from typing import Optional, Dict, Any
import json
import uuid

from .config import GatewayConfig
from .session import SessionManager, Session
from .router import MessageRouter, Message, MessageType
from .health import HealthMonitor, ComponentStatus
from dashboard.backend.swarm.orchestrator import SwarmOrchestrator
from dashboard.backend.routers.context import _context_trackers

logger = logging.getLogger(__name__)


class GatewayServer:
    """
    Gateway Server - Centralized control plane.
    
    Features:
    - WebSocket server on port 18789
    - Session management with persistence
    - Message routing between clients and agents
    - Health monitoring
    - Multi-client support
    """
    
    def __init__(self, config: Optional[GatewayConfig] = None):
        """
        Initialize gateway server.
        
        Args:
            config: Gateway configuration
        """
        self.config = config or GatewayConfig.from_env()
        
        # Initialize Socket.IO server
        self.sio = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins='*',
            logger=False,
            engineio_logger=False
        )
        
        # Initialize components
        self.session_manager = SessionManager(
            storage_backend=self.config.storage_backend,
            session_timeout=self.config.session_timeout
        )
        
        self.message_router = MessageRouter(
            queue_size=self.config.message_queue_size
        )
        
        self.health_monitor = HealthMonitor(
            check_interval=self.config.health_check_interval
        )
        
        # Phase 6: Swarm Orchestration integration for CLI commands
        self.orchestrator = SwarmOrchestrator()
        
        # Register Socket.IO event handlers
        self._register_handlers()
        
        logger.info(f"GatewayServer initialized on {self.config.host}:{self.config.port}")
    
    def _register_handlers(self):
        """Register Socket.IO event handlers"""
        
        @self.sio.event
        async def connect(sid, environ):
            """Handle client connection"""
            logger.info(f"Client connected: {sid}")
            
            # Create session for client
            session = await self.session_manager.create_session(
                session_id=sid,
                metadata={"sid": sid}
            )
            
            await self.sio.emit('connected', {
                'session_id': session.session_id,
                'message': 'Connected to Phantom Neural Cortex Gateway'
            }, to=sid)
            
            self.health_monitor.update_component_status('websocket', ComponentStatus.HEALTHY)
        
        @self.sio.event
        async def disconnect(sid):
            """Handle client disconnection"""
            logger.info(f"Client disconnected: {sid}")
            
            # Close session
            await self.session_manager.close_session(sid)
            
            # Clean up message queue
            self.message_router.remove_queue(sid)
        
        @self.sio.event
        async def message(sid, data):
            """Handle incoming message"""
            try:
                # Get session
                session = await self.session_manager.get_session(sid)
                if not session:
                    await self.sio.emit('error', {
                        'error': 'Session not found'
                    }, to=sid)
                    return
                
                # Parse message
                if isinstance(data, str):
                    data = json.loads(data)
                
                # Validate message type
                msg_type_str = data.get('type', 'user_message')
                try:
                    msg_type = MessageType(msg_type_str)
                except ValueError:
                    await self.sio.emit('error', {
                        'error': f'Invalid message type: {msg_type_str}',
                        'valid_types': [t.value for t in MessageType]
                    }, to=sid)
                    return

                # Validate content size
                content = data.get('content')
                if content and len(str(content)) > self.config.max_message_size:
                    await self.sio.emit('error', {
                        'error': 'Message content exceeds maximum size limit'
                    }, to=sid)
                    return
                
                # Create message object
                msg = Message(
                    message_id=data.get('message_id', f"msg_{sid}_{uuid.uuid4().hex[:8]}"),
                    session_id=sid,
                    type=msg_type,
                    content=content,
                    metadata=data.get('metadata', {})
                )
                
                # Route message
                success = await self.message_router.route_message(msg)
                
                if success:
                    await self.sio.emit('message_received', {
                        'message_id': msg.message_id,
                        'status': 'received'
                    }, to=sid)
                else:
                    await self.sio.emit('error', {
                        'error': 'Failed to route message'
                    }, to=sid)
            
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                await self.sio.emit('error', {
                    'error': f"Internal server error: {str(e)}"
                }, to=sid)
        
        @self.sio.event
        async def get_status(sid, data):
            """Handle status request"""
            try:
                health_status = await self.health_monitor.get_health_status(
                    self.session_manager,
                    self.message_router
                )
                
                await self.sio.emit('status', health_status.to_dict(), to=sid)
            
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                await self.sio.emit('error', {
                    'error': str(e)
                }, to=sid)
        
        @self.sio.event
        async def list_sessions(sid, data):
            """Handle list sessions request"""
            try:
                sessions = await self.session_manager.list_sessions()
                
                await self.sio.emit('sessions', {
                    'sessions': [s.to_dict() for s in sessions],
                    'count': len(sessions)
                }, to=sid)
            
            except Exception as e:
                logger.error(f"Error listing sessions: {e}")
                await self.sio.emit('error', {
                    'error': str(e)
                }, to=sid)
    
        @self.sio.event
        async def command(sid, data):
            """Handle CLI commands starting with / (Phase 6)"""
            try:
                if isinstance(data, str):
                    data = json.loads(data)
                
                cmd_text = data.get('command', '').strip()
                if not cmd_text.startswith('/'):
                    await self.sio.emit('error', {'error': 'Invalid command format. Use /command'}, to=sid)
                    return

                parts = cmd_text.split(' ', 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd == "/status":
                    # Get general system status
                    status = await self.health_monitor.get_health_status(self.session_manager, self.message_router)
                    await self.sio.emit('command_result', {
                        'command': cmd,
                        'result': status.to_dict()
                    }, to=sid)

                elif cmd == "/swarm-status":
                    # Get swarm stats
                    await self.sio.emit('command_result', {
                        'command': cmd,
                        'result': {
                            "active_tasks": len(self.orchestrator.active_tasks),
                            "agents": list(self.orchestrator.intelligence.agents.keys()),
                            "mode": "advanced_routing"
                        }
                    }, to=sid)

                elif cmd == "/preview":
                    if not args:
                        await self.sio.emit('error', {'error': 'Usage: /preview <task description>'}, to=sid)
                        return
                    
                    report = await self.orchestrator.get_impact_report(args)
                    await self.sio.emit('command_result', {
                        'command': cmd,
                        'result': report.model_dump()
                    }, to=sid)

                elif cmd == "/context":
                    # List context for current session
                    tracker = _context_trackers.get(sid)
                    if tracker:
                        await self.sio.emit('command_result', {
                            'command': cmd,
                            'result': {
                                "session_id": sid,
                                "total_tokens": tracker.context.total_tokens,
                                "usage_percent": (tracker.context.total_tokens / tracker.max_tokens) * 100
                            }
                        }, to=sid)
                    else:
                        await self.sio.emit('command_result', {'command': cmd, 'result': "No active context tracker for this session."}, to=sid)

                else:
                    await self.sio.emit('error', {'error': f"Unknown command: {cmd}"}, to=sid)

            except Exception as e:
                logger.error(f"Error handling command: {e}")
                await self.sio.emit('error', {'error': str(e)}, to=sid)

    async def start(self):
        """Start gateway server"""
        # Start components
        await self.session_manager.start()
        await self.health_monitor.start()
        
        logger.info(f"Gateway server started on {self.config.host}:{self.config.port}")
        
        # Update health status
        self.health_monitor.update_component_status('gateway', ComponentStatus.HEALTHY)
        self.health_monitor.update_component_status('session_manager', ComponentStatus.HEALTHY)
        self.health_monitor.update_component_status('message_router', ComponentStatus.HEALTHY)
    
    async def stop(self):
        """Stop gateway server"""
        # Stop components
        await self.health_monitor.stop()
        await self.session_manager.stop()
        
        logger.info("Gateway server stopped")
    
    def get_asgi_app(self):
        """Get ASGI application for deployment"""
        from fastapi import FastAPI
        
        app = FastAPI(title="Phantom Neural Cortex Gateway")
        
        # Mount Socket.IO
        socket_app = socketio.ASGIApp(self.sio, app)
        
        # Add REST endpoints
        @app.get("/health")
        async def health_check():
            """Health check endpoint"""
            health_status = await self.health_monitor.get_health_status(
                self.session_manager,
                self.message_router
            )
            return health_status.to_dict()
        
        @app.get("/sessions")
        async def list_sessions():
            """List active sessions"""
            sessions = await self.session_manager.list_sessions()
            return {
                'sessions': [s.to_dict() for s in sessions],
                'count': len(sessions)
            }
        
        @app.post("/sessions/{session_id}/close")
        async def close_session(session_id: str):
            """Close session"""
            success = await self.session_manager.close_session(session_id)
            return {'success': success}
        
        return socket_app


async def main():
    """Main entry point for standalone gateway server"""
    config = GatewayConfig.from_env()
    gateway = GatewayServer(config)
    
    await gateway.start()
    
    # Run server
    import uvicorn
    app = gateway.get_asgi_app()
    
    config_dict = {
        "host": config.host,
        "port": config.port,
        "log_level": "info"
    }
    
    server = uvicorn.Server(uvicorn.Config(app, **config_dict))
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        pass
    finally:
        await gateway.stop()


if __name__ == "__main__":
    asyncio.run(main())
