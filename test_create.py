#!/usr/bin/python3
"""Test create command"""
from console import HBNBCommand
import io
import sys

# Test create with parameters
cons = HBNBCommand()
captured = io.StringIO()
sys.stdout = captured
cons.onecmd('create State name="California"')
sys.stdout = sys.__stdout__
output = captured.getvalue()
print('Output:', repr(output))

from models import storage
print('Storage all:', list(storage.all().keys())[:5])

# Check the created state
if output.strip():
    key = 'State.' + output.strip()
    if key in storage.all():
        obj = storage.all()[key]
        print(f'State created: {obj}')
        print(f'State name: {obj.name if hasattr(obj, "name") else "NO NAME"}')
    else:
        print(f'Key {key} not found in storage')
else:
    print('No output from create command')
