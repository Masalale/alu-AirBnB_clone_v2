#!/usr/bin/python3
"""
console_2.py - Test create State and City with multiple parameters.
Demonstrates: Test create State name="California" + create City state_id="<new state ID>" name="Fremont" is present (more than one parameter) - FileStorage
"""
import subprocess
import sys
from models import storage

# Clear storage before test
for k in list(storage.all().keys()):
    del storage.all()[k]

print("Test: Create State and City with multiple parameters")
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

# Step 2: Create City with state_id and name parameters
print(f"\n2. Creating City with state_id='{state_id}' and name='Fremont'...")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'City', 
     f'state_id="{state_id}"', 'name="Fremont"'],
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
    # Verify the city was created with correct parameters
    key = f'City.{city_id}'
    if key in storage.all():
        city = storage.all()[key]
        city_state_id = getattr(city, 'state_id', None)
        city_name = getattr(city, 'name', None)
        
        if city_state_id == state_id and city_name == 'Fremont':
            print(f"   City state_id: {city_state_id}")
            print(f"   City name: {city_name}")
            print("✓ PASS: City created with correct parameters")
        else:
            print(f"✗ FAIL: Expected state_id='{state_id}' and name='Fremont'")
            print(f"        Got state_id='{city_state_id}' and name='{city_name}'")
            sys.exit(1)
    else:
        print(f"✗ FAIL: City {key} not found in storage")
        sys.exit(1)
else:
    print("✗ FAIL: City creation failed")
    sys.exit(1)

print("\nTest completed successfully!")
