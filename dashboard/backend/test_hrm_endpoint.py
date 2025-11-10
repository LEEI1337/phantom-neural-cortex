#!/usr/bin/env python3
"""Test HRM endpoints directly"""

from database import SessionLocal
from models import HRMPreset
from routers.hrm import get_hrm_presets

# Test database
db = SessionLocal()

try:
    print("Testing database query...")
    presets = db.query(HRMPreset).all()
    print(f"Found {len(presets)} presets in DB")

    for preset in presets:
        print(f"  - {preset.id}: {preset.name} ({preset.icon} {preset.color})")

    print("\nTesting get_hrm_presets endpoint...")
    # Simulate the endpoint call
    import asyncio
    result = asyncio.run(get_hrm_presets(db))
    print(f"Endpoint returned: {result}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
