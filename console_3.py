#!/usr/bin/python3
"""
console_3.py - Test create City with underscores converted to spaces.
Demonstrates: Test create State name="California" + create City state_id="<new state ID>" name="San_Francisco" is present (space translated to _) - FileStorage
"""
import subprocess
import sys
from models import storage

# Clear storage before test
for k in list(storage.all().keys()):
    del storage.all()[k]

print("Test: Create City with underscores converted to spaces")
print("-" * 50)

# Step 1: Create State with name parameter
print("\n1. Creating State with name='California'...")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'State', 'name="California"'],
    capture_output=True,
    text=True
)
state_id = result.stdout.strip()
print(f"   Created State ID: {state_id}")

if not state_id:
    print("✗ FAIL: State creation failed")
    sys.exit(1)

# Reload storage
try:
    storage.reload()
except Exception:
    pass

# Step 2: Create City with underscores in name (should be converted to spaces)
print(f"\n2. Creating City with name='San_Francisco'...")
print("   (Underscores should be converted to spaces)")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'City', 
     f'state_id="{state_id}"', 'name="San_Francisco"'],
    capture_output=True,
    text=True
)
city_id = result.stdout.strip()
print(f"   Created City ID: {city_id}")

# Reload storage again
try:
    storage.reload()
except Exception:
    pass

if city_id:
    # Verify the city was created with spaces instead of underscores
    key = f'City.{city_id}'
    if key in storage.all():
        city = storage.all()[key]
        city_name = getattr(city, 'name', None)
        
        # Underscores should be converted to spaces
        if city_name == 'San Francisco':
            print(f"   City name: '{city_name}'")
            print("✓ PASS: Underscores converted to spaces correctly")
        else:
            print(f"✗ FAIL: Expected name='San Francisco', got name='{city_name}'")
            sys.exit(1)
    else:
        print(f"✗ FAIL: City {key} not found in storage")
        sys.exit(1)
else:
    print("✗ FAIL: City creation failed")
    sys.exit(1)

print("\nTest completed successfully!")
