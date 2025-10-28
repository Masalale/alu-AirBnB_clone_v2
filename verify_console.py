#!/usr/bin/python3
"""Quick verification script for console create."""
import io
import sys
from models import storage
from console import HBNBCommand

# Clear storage
for k in list(storage.all().keys()):
    del storage.all()[k]

# Test create with parameters
cons = HBNBCommand()
captured = io.StringIO()
sys_stdout = sys.stdout
try:
    sys.stdout = captured
    cons.onecmd('create State name="California"')
finally:
    sys.stdout = sys_stdout

output = captured.getvalue().strip()
print(f"Output: '{output}'")

# Check storage
all_objs = storage.all()
print(f"Storage keys: {list(all_objs.keys())}")

if output and f'State.{output}' in all_objs:
    st = all_objs[f'State.{output}']
    print(f"State found! ID: {st.id}, Name: {st.name}")
    if st.name == 'California':
        print("SUCCESS: State created with correct name!")
    else:
        print(f"FAIL: Expected name='California', got name='{st.name}'")
else:
    print("FAIL: State not found in storage")
