#!/usr/bin/python3
"""
console_4.py - Full sequence: State, City, User, Place with integers and floats.
Demonstrates: Test create State name="California" + create City state_id="<new state ID>" name="San_Francisco_is_super_cool" + create User email="my@me.com" password="pwd" first_name="FN" last_name="LN" + create Place city_id="<new city ID>" user_id="<new user ID>" name="My_house" description="no_description_yet" number_rooms=4 number_bathrooms=1 max_guest=3 price_by_night=100 latitude=120.12 longitude=101.4 + show Place <new place ID> is present (integer + float) - FileStorage
"""
import subprocess
import sys
import io
from models import storage
from console import HBNBCommand

# Clear storage before test
for k in list(storage.all().keys()):
    del storage.all()[k]

print("Test: Full sequence with State, City, User, Place (integers + floats)")
print("=" * 70)

# Step 1: Create State
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

# Step 2: Create City
print(f"\n2. Creating City with name='San_Francisco_is_super_cool'...")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'City',
     f'state_id="{state_id}"', 'name="San_Francisco_is_super_cool"'],
    capture_output=True,
    text=True
)
city_id = result.stdout.strip()
print(f"   Created City ID: {city_id}")

if not city_id:
    print("✗ FAIL: City creation failed")
    sys.exit(1)

# Reload storage
try:
    storage.reload()
except Exception:
    pass

# Step 3: Create User
print(f"\n3. Creating User with email, password, first_name, last_name...")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'User',
     'email="my@me.com"', 'password="pwd"', 'first_name="FN"', 'last_name="LN"'],
    capture_output=True,
    text=True
)
user_id = result.stdout.strip()
print(f"   Created User ID: {user_id}")

if not user_id:
    print("✗ FAIL: User creation failed")
    sys.exit(1)

# Reload storage
try:
    storage.reload()
except Exception:
    pass

# Step 4: Create Place with integers and floats
print(f"\n4. Creating Place with integers and floats...")
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'Place',
     f'city_id="{city_id}"', f'user_id="{user_id}"',
     'name="My_house"', 'description="no_description_yet"',
     'number_rooms=4', 'number_bathrooms=1', 'max_guest=3',
     'price_by_night=100', 'latitude=120.12', 'longitude=101.4'],
    capture_output=True,
    text=True
)
place_id = result.stdout.strip()
print(f"   Created Place ID: {place_id}")

if not place_id:
    print("✗ FAIL: Place creation failed")
    sys.exit(1)

# Reload storage
try:
    storage.reload()
except Exception:
    pass

# Verify Place attributes
print(f"\n5. Verifying Place attributes...")
key = f'Place.{place_id}'
if key in storage.all():
    place = storage.all()[key]
    
    # Check string attributes (underscores converted to spaces)
    name = getattr(place, 'name', None)
    description = getattr(place, 'description', None)
    
    # Check integer attributes
    number_rooms = getattr(place, 'number_rooms', None)
    number_bathrooms = getattr(place, 'number_bathrooms', None)
    max_guest = getattr(place, 'max_guest', None)
    
    # Check float attributes
    price_by_night = getattr(place, 'price_by_night', None)
    latitude = getattr(place, 'latitude', None)
    longitude = getattr(place, 'longitude', None)
    
    print(f"   name: '{name}' (expected: 'My house')")
    print(f"   description: '{description}' (expected: 'no description yet')")
    print(f"   number_rooms: {number_rooms} (expected: 4)")
    print(f"   number_bathrooms: {number_bathrooms} (expected: 1)")
    print(f"   max_guest: {max_guest} (expected: 3)")
    print(f"   price_by_night: {price_by_night} (expected: 100.0)")
    print(f"   latitude: {latitude} (expected: 120.12)")
    print(f"   longitude: {longitude} (expected: 101.4)")
    
    # Verify values
    checks = [
        (name == 'My house', "name should be 'My house'"),
        (description == 'no description yet', "description should be 'no description yet'"),
        (number_rooms is not None and int(number_rooms) == 4, "number_rooms should be 4"),
        (number_bathrooms is not None and int(number_bathrooms) == 1, "number_bathrooms should be 1"),
        (max_guest is not None and int(max_guest) == 3, "max_guest should be 3"),
        (price_by_night is not None and abs(float(price_by_night) - 100.0) < 0.01, "price_by_night should be 100.0"),
        (latitude is not None and abs(float(latitude) - 120.12) < 0.01, "latitude should be 120.12"),
        (longitude is not None and abs(float(longitude) - 101.4) < 0.01, "longitude should be 101.4"),
    ]
    
    all_pass = all(check[0] for check in checks)
    if not all_pass:
        for check, msg in checks:
            if not check:
                print(f"   ✗ {msg}")
        sys.exit(1)
    
    print("   ✓ All attributes verified correctly")
else:
    print(f"✗ FAIL: Place {key} not found in storage")
    sys.exit(1)

# Step 5: Test show command
print(f"\n6. Running 'show Place {place_id}'...")
cons = HBNBCommand()
captured = io.StringIO()
sys_stdout = sys.stdout
try:
    sys.stdout = captured
    cons.onecmd(f'show Place {place_id}')
finally:
    sys.stdout = sys_stdout

output = captured.getvalue().strip()
print(f"   Output: {output}")

# Verify output contains place ID and name with spaces
if place_id in output and 'My house' in output:
    print("   ✓ show command output contains ID and name with spaces")
else:
    print(f"   ✗ show command output missing ID or 'My house'")
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED!")
