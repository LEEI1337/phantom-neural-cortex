"""
WebSocket Router
Real-time updates via Socket.IO
"""

import socketio

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:3000', 'http://localhost:5173']
)

# Connection event
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_status', {'connected': True}, room=sid)

# Disconnection event
@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Subscribe to project updates
@sio.event
async def subscribe_project(sid, data):
    project_id = data.get('project_id')
    if project_id:
        await sio.enter_room(sid, f"project_{project_id}")
        print(f"Client {sid} subscribed to project {project_id}")

# Unsubscribe from project
@sio.event
async def unsubscribe_project(sid, data):
    project_id = data.get('project_id')
    if project_id:
        await sio.leave_room(sid, f"project_{project_id}")
        print(f"Client {sid} unsubscribed from project {project_id}")

# Utility functions for emitting events
async def emit_task_update(task_id: str, data: dict):
    """Emit task update to all connected clients"""
    await sio.emit('task_update', {
        'task_id': task_id,
        **data
    })

async def emit_feedback_loop_update(task_id: str, data: dict):
    """Emit feedback loop update"""
    await sio.emit('feedback_loop', {
        'task_id': task_id,
        **data
    })

async def emit_agent_switch(task_id: str, from_agent: str, to_agent: str, reason: str):
    """Emit agent switch event"""
    await sio.emit('agent_switch', {
        'task_id': task_id,
        'from_agent': from_agent,
        'to_agent': to_agent,
        'reason': reason
    })

async def emit_system_alert(message: str, severity: str = 'info'):
    """Emit system-wide alert"""
    await sio.emit('system_alert', {
        'message': message,
        'severity': severity
    })
