#!/usr/bin/python3
"""
console_0.py - Test regular create State (without parameters).
Demonstrates: Test create State is present (regular case) - FileStorage
"""
import subprocess
import sys

# Test 1: Regular create State (no params)
print("Test: Create State (regular case, no parameters)")
print("-" * 50)
result = subprocess.run(
    [sys.executable, 'create_fake_console.py', 'create', 'State'],
    capture_output=True,
    text=True
)
state_id = result.stdout.strip()
print(f"Created State ID: {state_id}")
if state_id:
    print("✓ PASS: State created successfully")
else:
    print("✗ FAIL: State creation failed")
    sys.exit(1)

print("\nTest completed successfully!")
