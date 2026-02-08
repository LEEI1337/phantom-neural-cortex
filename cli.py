import asyncio
import socketio
import json
import sys
from typing import Optional

class CortexCLI:
    """
    CLI client for Phantom Neural Cortex (Phase 6).
    Connects to the Gateway on port 18789.
    """
    
    def __init__(self, url: str = "http://localhost:18789"):
        self.sio = socketio.AsyncClient()
        self.url = url
        self.session_id: Optional[str] = None
        
        self._setup_handlers()
        
    def _setup_handlers(self):
        @self.sio.event
        async def connect():
            print("🟢 Connected to Gateway")
            
        @self.sio.event
        async def connected(data):
            self.session_id = data.get('session_id')
            print(f"🆔 Session: {self.session_id}")
            
        @self.sio.event
        async def command_result(data):
            cmd = data.get('command')
            result = data.get('result')
            print(f"\n--- Result for {cmd} ---")
            print(json.dumps(result, indent=2))
            print("-" * 25)
            print("\ncortex> ", end="", flush=True)

        @self.sio.event
        async def error(data):
            print(f"❌ Error: {data.get('error')}")
            print("\ncortex> ", end="", flush=True)

        @self.sio.event
        async def message(data):
            print(f"\n[Agent] {data.get('content')}")
            print("\ncortex> ", end="", flush=True)

    async def run(self):
        try:
            await self.sio.connect(self.url)
        except Exception as e:
            print(f"Failed to connect to gateway at {self.url}: {e}")
            return

        print("\n🚀 Phantom Neural Cortex CLI v3.0")
        print("Type /status, /swarm-status, /preview <task>, or /context")
        print("Type 'exit' to quit\n")

        while True:
            try:
                # Use run_in_executor to avoid blocking the event loop with input()
                line = await asyncio.get_event_loop().run_in_executor(None, lambda: input("cortex> "))
                
                if not line:
                    continue
                    
                if line.lower() in ['exit', 'quit']:
                    break
                    
                if line.startswith('/'):
                    await self.sio.emit('command', {'command': line})
                else:
                    await self.sio.emit('message', {'content': line, 'type': 'user_message'})
                    
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

        await self.sio.disconnect()
        print("Bye!")

if __name__ == "__main__":
    cli = CortexCLI()
    asyncio.run(cli.run())
