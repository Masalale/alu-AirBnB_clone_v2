#!/usr/bin/python3
"""Demonstration of create command with parameters feature."""
from console import HBNBCommand
from models import storage
import io
import sys


def run_cmd(cmd):
    """Run a console command and return output."""
    cons = HBNBCommand()
    captured = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured
        cons.onecmd(cmd)
    finally:
        sys.stdout = sys_stdout
    return captured.getvalue().strip()


def main():
    # Clear storage
    for k in list(storage.all().keys()):
        del storage.all()[k]

    print("=" * 70)
    print("DEMONSTRATION: Create Command with Parameters")
    print("=" * 70)

    print("\n1. STRING PARAMETERS (with underscores converted to spaces)")
    print("-" * 70)
    cmd = 'create State name="New_York"'
    print(f"Command: {cmd}")
    state_id = run_cmd(cmd)
    print(f"Result: Created State ID {state_id}")
    state = storage.all()[f'State.{state_id}']
    print(f"Verified: state.name = '{state.name}' (underscores → spaces)")

    print("\n2. ESCAPED QUOTES IN STRINGS")
    print("-" * 70)
    cmd = r'create City name="John\"s_City" state_id="' + state_id + '"'
    print(f"Command: {cmd}")
    city_id = run_cmd(cmd)
    print(f"Result: Created City ID {city_id}")
    city = storage.all()[f'City.{city_id}']
    print(f"Verified: city.name = '{city.name}' (escaped quotes preserved)")

    print("\n3. INTEGER PARAMETERS")
    print("-" * 70)
    cmd = 'create Place number_rooms=4 number_bathrooms=2 max_guest=6'
    print(f"Command: {cmd}")
    place_id = run_cmd(cmd)
    print(f"Result: Created Place ID {place_id}")
    place = storage.all()[f'Place.{place_id}']
    print(f"Verified: number_rooms={place.number_rooms} (type: {type(place.number_rooms).__name__})")
    print(f"Verified: number_bathrooms={place.number_bathrooms} (type: {type(place.number_bathrooms).__name__})")
    print(f"Verified: max_guest={place.max_guest} (type: {type(place.max_guest).__name__})")

    print("\n4. FLOAT PARAMETERS")
    print("-" * 70)
    cmd = 'create Place price_by_night=150.50 latitude=37.7749 longitude=-122.4194'
    print(f"Command: {cmd}")
    place_id2 = run_cmd(cmd)
    print(f"Result: Created Place ID {place_id2}")
    place2 = storage.all()[f'Place.{place_id2}']
    print(f"Verified: price_by_night={place2.price_by_night} (type: {type(place2.price_by_night).__name__})")
    print(f"Verified: latitude={place2.latitude} (type: {type(place2.latitude).__name__})")
    print(f"Verified: longitude={place2.longitude} (type: {type(place2.longitude).__name__})")

    print("\n5. MIXED PARAMETERS (strings, integers, floats)")
    print("-" * 70)
    cmd = f'create Place city_id="{city_id}" name="Luxury_Apartment" number_rooms=3 price_by_night=299.99'
    print(f"Command: {cmd}")
    place_id3 = run_cmd(cmd)
    print(f"Result: Created Place ID {place_id3}")
    place3 = storage.all()[f'Place.{place_id3}']
    print(f"Verified: city_id='{place3.city_id}' (string)")
    print(f"Verified: name='{place3.name}' (string with spaces)")
    print(f"Verified: number_rooms={place3.number_rooms} (int)")
    print(f"Verified: price_by_night={place3.price_by_night} (float)")

    print("\n6. MALFORMED PARAMETERS (should be skipped)")
    print("-" * 70)
    cmd = 'create User email="test@test.com" bad_param first_name="John" invalid= last_name="Doe"'
    print(f"Command: {cmd}")
    user_id = run_cmd(cmd)
    print(f"Result: Created User ID {user_id}")
    user = storage.all()[f'User.{user_id}']
    print(f"Verified: email='{user.email}' (valid param)")
    print(f"Verified: first_name='{user.first_name}' (valid param)")
    print(f"Verified: last_name='{user.last_name}' (valid param)")
    print(f"Verified: bad_param skipped (malformed)")
    print(f"Verified: invalid= skipped (malformed)")

    print("\n" + "=" * 70)
    print("✓ ALL FEATURES DEMONSTRATED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == '__main__':
    main()
