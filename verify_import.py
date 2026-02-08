
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

print(f"Path: {sys.path[0]}")

try:
    print("Importing dashboard.backend.database...")
    import dashboard.backend.database
    print("Success!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")
