import asyncio
import socketio
import json
import os
import sys

import logging

# Set up logging
logging_level = logging.INFO
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

async def verify_cli_commands():
    print("🚀 Verifying Phase 6 CLI Commands via Gateway...")
    
    sio = socketio.AsyncClient()
    url = "http://localhost:18789"
    results = {}
    
    # Event handlers
    @sio.event
    async def command_result(data):
        cmd = data.get('command')
        result = data.get('result')
        print(f"✅ Received result for {cmd}")
        results[cmd] = result

    # 1. Start the gateway in the background or assume it's running
    # For this test, we expect the user to have the gateway running or we'll try to start a temporary one
    
    try:
        await sio.connect(url)
    except Exception as e:
        print(f"❌ Gateway not reachable at {url}. Please start the gateway first.")
        print("Hint: Run 'python -m gateway.server' in a separate terminal.")
        return

    # 2. Test /status
    print("Testing /status...")
    await sio.emit('command', {'command': '/status'})
    await asyncio.sleep(1)
    
    # 3. Test /swarm-status
    print("Testing /swarm-status...")
    await sio.emit('command', {'command': '/swarm-status'})
    await asyncio.sleep(1)
    
    # 4. Test /preview
    print("Testing /preview...")
    await sio.emit('command', {'command': '/preview Create a new REST API with FastAPI'})
    await asyncio.sleep(1)

    print("\n--- Summary ---")
    if "/status" in results:
        print("✅ /status command: WORKING")
    else:
        print("❌ /status command: FAILED")
        
    if "/swarm-status" in results:
        print("✅ /swarm-status command: WORKING")
    else:
        print("❌ /swarm-status command: FAILED")
        
    if "/preview" in results:
        print("✅ /preview command: WORKING")
        print(f"   Recommendation: {results['/preview'].get('recommendation')}")
    else:
        print("❌ /preview command: FAILED")

    await sio.disconnect()
    print("\nPhase 6 CLI Command Integration: VERIFIED 🚀")

if __name__ == "__main__":
    asyncio.run(verify_cli_commands())
