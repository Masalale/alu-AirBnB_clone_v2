#!/usr/bin/python3
"""
console_1.py - Test create State with name parameter.
Demonstrates: Test create State name="California" is present (new feature) - FileStorage
"""
import subprocess
import sys
from models import storage

# Clear storage before test
for k in list(storage.all().keys()):
    del storage.all()[k]

print("Test: Create State with name parameter")
print("-" * 50)
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'State', 'name="California"'],
    capture_output=True,
    text=True
)
state_id = result.stdout.strip()
print(f"Created State ID: {state_id}")

if state_id:
    # Reload storage to pick up changes from subprocess
    try:
        storage.reload()
    except Exception:
        pass
    
    # Verify the state was created with the name parameter
    key = f'State.{state_id}'
    if key in storage.all():
        state = storage.all()[key]
        name = getattr(state, 'name', None)
        if name == 'California':
            print(f"State name: {name}")
            print("✓ PASS: State created with name='California'")
        else:
            print(f"✗ FAIL: Expected name='California', got name='{name}'")
            sys.exit(1)
    else:
        print(f"✗ FAIL: State {key} not found in storage")
        sys.exit(1)
else:
    print("✗ FAIL: State creation failed")
    sys.exit(1)

print("\nTest completed successfully!")
