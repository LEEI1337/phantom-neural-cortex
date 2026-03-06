"""Run a Phantom Agent from AGENT.yaml config.

Usage:
    python run_agent.py --config config/templates/lisa01.yaml
    python run_agent.py --config agents/lisa01/AGENT.yaml --gateway
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("phantom-agent")


async def run(config_path: str, with_gateway: bool = False):
    """Start a Phantom Agent."""
    from agent import PhantomAgent
    from killswitch.handler import KillReason

    agent = PhantomAgent.from_config(config_path)
    logger.info(f"Loaded agent: {agent.name} ({agent.role})")

    # Setup signal handlers for terminal killswitch
    loop = asyncio.get_running_loop()

    def signal_handler(sig):
        logger.warning(f"Signal {sig} received — activating killswitch")
        asyncio.ensure_future(
            agent.killswitch.kill(
                reason=KillReason.TERMINAL,
                triggered_by="system",
                details=f"Signal {sig}",
            )
        )
        asyncio.ensure_future(agent.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: signal_handler(s))

    await agent.start()

    if with_gateway:
        from gateway.server import GatewayServer
        import uvicorn

        gateway = GatewayServer()
        gateway.register_agent(agent)
        await gateway.start()

        app = gateway.get_asgi_app()
        config = uvicorn.Config(app, host="0.0.0.0", port=18789, log_level="info")
        server = uvicorn.Server(config)

        try:
            await server.serve()
        finally:
            await gateway.stop()
            await agent.stop()
    else:
        # Standalone mode — keep running until killed
        try:
            while agent._running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            await agent.stop()


def main():
    parser = argparse.ArgumentParser(description="Run a Phantom Agent")
    parser.add_argument("--config", required=True, help="Path to AGENT.yaml")
    parser.add_argument("--gateway", action="store_true", help="Also start the PNC Gateway")
    args = parser.parse_args()

    try:
        asyncio.run(run(args.config, with_gateway=args.gateway))
    except KeyboardInterrupt:
        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()
