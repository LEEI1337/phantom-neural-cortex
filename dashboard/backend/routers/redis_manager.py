"""
Redis State Manager for Multi-Agent Coordination

Provides:
- Distributed state management across multiple processes
- Pub/Sub for cross-process WebSocket broadcasting
- Agent coordination and task state synchronization
- <50ms latency for state operations
"""

import redis.asyncio as redis
from typing import Dict, Any, Optional, List
import json
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)


class RedisStateManager:
    """
    Redis-based state manager for distributed multi-agent coordination.

    Features:
    - Async Redis operations (<50ms latency)
    - Pub/Sub for cross-process event broadcasting
    - Task state synchronization
    - Agent coordination (locks, semaphores)
    - Connection pooling for performance
    """

    def __init__(self):
        # Redis connection URL from environment
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

        # Connection pool for better performance
        self.pool = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=20,
            decode_responses=True,  # Auto-decode bytes to str
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30
        )

        # Redis client
        self.redis: Optional[redis.Redis] = None

        # PubSub client (separate connection)
        self.pubsub: Optional[redis.client.PubSub] = None

        logger.info(f"RedisStateManager initialized with URL: {redis_url.split('@')[-1] if '@' in redis_url else 'localhost:6379'}")

    async def connect(self):
        """
        Initialize Redis connections.

        Should be called on application startup.
        """
        try:
            # Create Redis client from pool
            self.redis = redis.Redis(connection_pool=self.pool)

            # Test connection
            await self.redis.ping()

            # Create PubSub client
            self.pubsub = self.redis.pubsub()

            logger.info("Redis connected successfully")

        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    async def disconnect(self):
        """
        Close Redis connections.

        Should be called on application shutdown.
        """
        try:
            if self.pubsub:
                await self.pubsub.close()

            if self.redis:
                await self.redis.close()

            if self.pool:
                await self.pool.disconnect()

            logger.info("Redis disconnected")

        except Exception as e:
            logger.error(f"Redis disconnect error: {e}")

    # ========================================================================
    # STATE MANAGEMENT
    # ========================================================================

    async def set_state(self, key: str, value: Any, ttl: int = None):
        """
        Set state value in Redis.

        Args:
            key: State key (e.g., "task:123:status")
            value: Value (will be JSON-serialized)
            ttl: Optional time-to-live in seconds

        Example:
            await redis_manager.set_state("task:123:status", {"status": "running"}, ttl=3600)
        """
        try:
            # Serialize value to JSON
            serialized = json.dumps(value) if not isinstance(value, str) else value

            # Set with optional TTL
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)

            logger.debug(f"State set: {key}")

        except Exception as e:
            logger.error(f"Failed to set state {key}: {e}")
            raise

    async def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get state value from Redis.

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            Deserialized value or default

        Example:
            status = await redis_manager.get_state("task:123:status")
        """
        try:
            value = await self.redis.get(key)

            if value is None:
                return default

            # Try to deserialize as JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

        except Exception as e:
            logger.error(f"Failed to get state {key}: {e}")
            return default

    async def delete_state(self, key: str):
        """Delete state key."""
        try:
            await self.redis.delete(key)
            logger.debug(f"State deleted: {key}")
        except Exception as e:
            logger.error(f"Failed to delete state {key}: {e}")

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Failed to check existence of {key}: {e}")
            return False

    # ========================================================================
    # HASH OPERATIONS (for complex objects)
    # ========================================================================

    async def hset(self, key: str, field: str, value: Any):
        """
        Set hash field.

        Example:
            await redis_manager.hset("task:123", "agent", "claude")
        """
        try:
            serialized = json.dumps(value) if not isinstance(value, str) else value
            await self.redis.hset(key, field, serialized)
        except Exception as e:
            logger.error(f"Failed to set hash field {key}:{field}: {e}")

    async def hget(self, key: str, field: str, default: Any = None) -> Any:
        """Get hash field."""
        try:
            value = await self.redis.hget(key, field)

            if value is None:
                return default

            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

        except Exception as e:
            logger.error(f"Failed to get hash field {key}:{field}: {e}")
            return default

    async def hgetall(self, key: str) -> Dict[str, Any]:
        """Get all hash fields."""
        try:
            data = await self.redis.hgetall(key)

            # Deserialize all values
            result = {}
            for field, value in data.items():
                try:
                    result[field] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    result[field] = value

            return result

        except Exception as e:
            logger.error(f"Failed to get all hash fields for {key}: {e}")
            return {}

    # ========================================================================
    # PUB/SUB FOR CROSS-PROCESS COMMUNICATION
    # ========================================================================

    async def publish(self, channel: str, message: Dict[str, Any]):
        """
        Publish message to Redis channel (cross-process broadcast).

        Args:
            channel: Channel name (e.g., "events:global", "events:task:123")
            message: Message dict (will be JSON-serialized)

        Example:
            await redis_manager.publish("events:global", {
                "type": "task_update",
                "task_id": "123",
                "status": "completed"
            })
        """
        try:
            # Add timestamp
            message_with_timestamp = {
                **message,
                "redis_timestamp": datetime.utcnow().isoformat()
            }

            serialized = json.dumps(message_with_timestamp)

            # Publish to channel
            subscribers = await self.redis.publish(channel, serialized)

            logger.debug(f"Published to {channel} ({subscribers} subscribers)")

        except Exception as e:
            logger.error(f"Failed to publish to {channel}: {e}")

    async def subscribe(self, *channels: str):
        """
        Subscribe to Redis channels.

        Args:
            channels: Channel names to subscribe to

        Example:
            await redis_manager.subscribe("events:global", "events:task:123")
        """
        try:
            await self.pubsub.subscribe(*channels)
            logger.info(f"Subscribed to channels: {channels}")
        except Exception as e:
            logger.error(f"Failed to subscribe to channels: {e}")

    async def unsubscribe(self, *channels: str):
        """Unsubscribe from channels."""
        try:
            await self.pubsub.unsubscribe(*channels)
            logger.info(f"Unsubscribed from channels: {channels}")
        except Exception as e:
            logger.error(f"Failed to unsubscribe: {e}")

    async def listen(self) -> Dict[str, Any]:
        """
        Listen for messages on subscribed channels (async generator).

        Yields:
            Message dict with 'type', 'channel', 'data'

        Example:
            async for message in redis_manager.listen():
                print(f"Received on {message['channel']}: {message['data']}")
        """
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    # Deserialize message data
                    try:
                        data = json.loads(message["data"])
                        yield {
                            "type": "message",
                            "channel": message["channel"],
                            "data": data
                        }
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.error(f"Failed to deserialize message: {e}")

        except Exception as e:
            logger.error(f"Error listening to pubsub: {e}")

    # ========================================================================
    # AGENT COORDINATION
    # ========================================================================

    async def acquire_lock(self, resource: str, timeout: int = 10) -> bool:
        """
        Acquire distributed lock.

        Args:
            resource: Resource name (e.g., "task:123:processing")
            timeout: Lock timeout in seconds

        Returns:
            True if lock acquired, False otherwise

        Example:
            if await redis_manager.acquire_lock("task:123", timeout=60):
                try:
                    # Process task
                    pass
                finally:
                    await redis_manager.release_lock("task:123")
        """
        try:
            lock_key = f"lock:{resource}"
            result = await self.redis.set(lock_key, "1", ex=timeout, nx=True)
            return result is not None

        except Exception as e:
            logger.error(f"Failed to acquire lock for {resource}: {e}")
            return False

    async def release_lock(self, resource: str):
        """Release distributed lock."""
        try:
            lock_key = f"lock:{resource}"
            await self.redis.delete(lock_key)
        except Exception as e:
            logger.error(f"Failed to release lock for {resource}: {e}")

    async def increment_counter(self, key: str, amount: int = 1) -> int:
        """
        Atomic counter increment.

        Returns:
            New counter value

        Example:
            task_count = await redis_manager.increment_counter("tasks:completed")
        """
        try:
            return await self.redis.incrby(key, amount)
        except Exception as e:
            logger.error(f"Failed to increment counter {key}: {e}")
            return 0

    async def get_counter(self, key: str) -> int:
        """Get counter value."""
        try:
            value = await self.redis.get(key)
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"Failed to get counter {key}: {e}")
            return 0

    # ========================================================================
    # TASK STATE MANAGEMENT
    # ========================================================================

    async def set_task_state(self, task_id: str, state: Dict[str, Any], ttl: int = 86400):
        """
        Set task state (auto-expires after 24h by default).

        Args:
            task_id: Task ID
            state: Task state dict
            ttl: TTL in seconds (default: 24 hours)
        """
        key = f"task:{task_id}:state"
        await self.set_state(key, state, ttl=ttl)

    async def get_task_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task state."""
        key = f"task:{task_id}:state"
        return await self.get_state(key)

    async def update_task_field(self, task_id: str, field: str, value: Any):
        """Update specific task field."""
        key = f"task:{task_id}:state"
        await self.hset(key, field, value)

    async def get_active_tasks(self, agent: str = None) -> List[str]:
        """
        Get list of active task IDs.

        Args:
            agent: Optional agent filter

        Returns:
            List of task IDs
        """
        try:
            # Scan for task keys
            pattern = "task:*:state"
            task_ids = []

            cursor = 0
            while True:
                cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)

                for key in keys:
                    # Extract task ID from key
                    task_id = key.split(":")[1]

                    # Filter by agent if specified
                    if agent:
                        task_agent = await self.hget(key, "agent")
                        if task_agent == agent:
                            task_ids.append(task_id)
                    else:
                        task_ids.append(task_id)

                if cursor == 0:
                    break

            return task_ids

        except Exception as e:
            logger.error(f"Failed to get active tasks: {e}")
            return []

    # ========================================================================
    # HEALTH & MONITORING
    # ========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """
        Check Redis health and return stats.

        Returns:
            Health status dict
        """
        try:
            # Ping test
            start = datetime.utcnow()
            await self.redis.ping()
            latency_ms = (datetime.utcnow() - start).total_seconds() * 1000

            # Get info
            info = await self.redis.info()

            return {
                "status": "healthy",
                "latency_ms": round(latency_ms, 2),
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
                "total_commands_processed": info.get("total_commands_processed"),
                "uptime_days": info.get("uptime_in_days")
            }

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global RedisStateManager instance
redis_manager = RedisStateManager()
