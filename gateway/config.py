"""
Gateway Configuration

Configuration settings for the gateway service.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field


class GatewayConfig(BaseModel):
    """Gateway configuration settings"""
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Gateway host")
    port: int = Field(default=18789, description="Gateway port")
    
    # Session settings
    session_timeout: int = Field(default=3600, description="Session timeout in seconds")
    max_sessions: int = Field(default=1000, description="Maximum concurrent sessions")
    
    # Storage settings
    storage_backend: str = Field(default="redis", description="Storage backend (redis, sqlite, postgres)")
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")
    database_url: Optional[str] = Field(default=None, description="Database connection URL")
    
    # Message routing
    max_message_size: int = Field(default=10485760, description="Max message size (10MB)")
    message_queue_size: int = Field(default=1000, description="Message queue size per session")
    
    # Health monitoring
    health_check_interval: int = Field(default=30, description="Health check interval in seconds")
    
    @classmethod
    def from_env(cls) -> "GatewayConfig":
        """Load configuration from environment variables"""
        return cls(
            host=os.getenv("GATEWAY_HOST", "0.0.0.0"),
            port=int(os.getenv("GATEWAY_PORT", "18789")),
            session_timeout=int(os.getenv("GATEWAY_SESSION_TIMEOUT", "3600")),
            max_sessions=int(os.getenv("GATEWAY_MAX_SESSIONS", "1000")),
            storage_backend=os.getenv("GATEWAY_STORAGE_BACKEND", "redis"),
            redis_url=os.getenv("REDIS_URL"),
            database_url=os.getenv("DATABASE_URL"),
            max_message_size=int(os.getenv("GATEWAY_MAX_MESSAGE_SIZE", "10485760")),
            message_queue_size=int(os.getenv("GATEWAY_MESSAGE_QUEUE_SIZE", "1000")),
            health_check_interval=int(os.getenv("GATEWAY_HEALTH_CHECK_INTERVAL", "30")),
        )
