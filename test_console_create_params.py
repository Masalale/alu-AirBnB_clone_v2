#!/usr/bin/python3
"""Test console create command with parameters"""

from console import HBNBCommand
from models import storage
from models.state import State

# Create console instance
cmd = HBNBCommand()

# Test 1: Create State with name parameter
print("Test 1: create State name=\"California\"")
cmd.onecmd('create State name="California"')

# Get all states and check if name was set correctly
all_objs = storage.all()
states = [obj for obj in all_objs.values() if isinstance(obj, State)]
if states:
    last_state = states[-1]
    print(f"State created: id={last_state.id}, name={last_state.name}")
else:
    print("No states found!")

# Test 2: Create State with name containing spaces
print("\nTest 2: create State name=\"New_York\"")
cmd.onecmd('create State name="New_York"')

all_objs = storage.all()
states = [obj for obj in all_objs.values() if isinstance(obj, State)]
if len(states) >= 2:
    last_state = states[-1]
    print(f"State created: id={last_state.id}, name={last_state.name}")
else:
    print("State not created!")

# Test 3: Create State with escaped quotes
print("\nTest 3: create State name=\"New_\\\"York\\\"\"")
cmd.onecmd('create State name="New_\\"York\\""')

all_objs = storage.all()
states = [obj for obj in all_objs.values() if isinstance(obj, State)]
if len(states) >= 3:
    last_state = states[-1]
    print(f"State created: id={last_state.id}, name={last_state.name}")
else:
    print("State not created!")
