"""Killswitch System — 3-way emergency stop.

1. Terminal: Ctrl+K → SIGTERM
2. Mattermost: /killswitch <agent> → Webhook
3. API: POST /agent/<name>/kill → PNC stops task
"""

from .handler import KillswitchHandler, KillReason
from .api import killswitch_router

__all__ = ["KillswitchHandler", "KillReason", "killswitch_router"]
