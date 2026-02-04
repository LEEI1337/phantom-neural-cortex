"""
Health Monitor

Monitors gateway health and provides health check endpoints.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ComponentStatus(str, Enum):
    """Component status enum"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthStatus:
    """Health status data model"""
    status: ComponentStatus
    uptime_seconds: float
    active_sessions: int
    message_queue_size: int
    memory_usage_mb: float
    last_check: datetime
    components: Dict[str, ComponentStatus]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['status'] = self.status.value
        data['last_check'] = self.last_check.isoformat()
        data['components'] = {k: v.value for k, v in self.components.items()}
        return data


class HealthMonitor:
    """
    Monitors gateway health.
    
    Features:
    - Component health checks
    - Uptime tracking
    - Resource usage monitoring
    - Automatic health status determination
    """
    
    def __init__(self, check_interval: int = 30):
        """
        Initialize health monitor.
        
        Args:
            check_interval: Health check interval in seconds
        """
        self.check_interval = check_interval
        self.start_time = datetime.now()
        
        # Component health
        self._component_status: Dict[str, ComponentStatus] = {}
        
        # Health check task
        self._check_task: Optional[asyncio.Task] = None
        
        logger.info("HealthMonitor initialized")
    
    async def start(self):
        """Start health monitoring"""
        self._check_task = asyncio.create_task(self._health_check_loop())
        logger.info("HealthMonitor started")
    
    async def stop(self):
        """Stop health monitoring"""
        if self._check_task:
            self._check_task.cancel()
            try:
                await self._check_task
            except asyncio.CancelledError:
                pass
        logger.info("HealthMonitor stopped")
    
    def update_component_status(self, component: str, status: ComponentStatus):
        """
        Update component health status.
        
        Args:
            component: Component name
            status: Health status
        """
        self._component_status[component] = status
        logger.debug(f"Component {component} status: {status.value}")
    
    async def get_health_status(
        self,
        session_manager = None,
        message_router = None
    ) -> HealthStatus:
        """
        Get current health status.
        
        Args:
            session_manager: Session manager instance
            message_router: Message router instance
            
        Returns:
            Health status
        """
        # Calculate uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Get metrics
        active_sessions = 0
        if session_manager:
            sessions = await session_manager.list_sessions()
            active_sessions = len(sessions)
        
        message_queue_size = 0
        if message_router:
            # Sum all queue sizes
            for session_id in message_router._queues:
                message_queue_size += message_router.get_queue_size(session_id)
        
        # Get memory usage (simplified)
        memory_usage_mb = 0.0
        try:
            import psutil
            process = psutil.Process()
            memory_usage_mb = process.memory_info().rss / 1024 / 1024
        except ImportError:
            pass
        
        # Determine overall status
        overall_status = self._determine_overall_status()
        
        return HealthStatus(
            status=overall_status,
            uptime_seconds=uptime,
            active_sessions=active_sessions,
            message_queue_size=message_queue_size,
            memory_usage_mb=memory_usage_mb,
            last_check=datetime.now(),
            components=self._component_status.copy()
        )
    
    def _determine_overall_status(self) -> ComponentStatus:
        """Determine overall health status from components"""
        if not self._component_status:
            return ComponentStatus.UNKNOWN
        
        statuses = list(self._component_status.values())
        
        # If any component is unhealthy, overall is unhealthy
        if ComponentStatus.UNHEALTHY in statuses:
            return ComponentStatus.UNHEALTHY
        
        # If any component is degraded, overall is degraded
        if ComponentStatus.DEGRADED in statuses:
            return ComponentStatus.DEGRADED
        
        # All components healthy
        return ComponentStatus.HEALTHY
    
    async def _health_check_loop(self):
        """Background health check loop"""
        while True:
            try:
                await asyncio.sleep(self.check_interval)
                
                # Perform health checks
                await self._perform_health_checks()
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
    
    async def _perform_health_checks(self):
        """Perform health checks on all components"""
        # TODO: Implement specific health checks
        # For now, assume all components are healthy
        pass
