#!/usr/bin/python3
"""Simple manual test for console create command"""

# Test the parsing logic directly
args = 'State name="California"'

# Parse args to handle quoted values with spaces
tokens = []
current_token = []
in_quotes = False

for char in args:
    if char == '"':
        in_quotes = not in_quotes
        current_token.append(char)
    elif char == ' ' and not in_quotes:
        if current_token:
            tokens.append(''.join(current_token))
            current_token = []
    else:
        current_token.append(char)

# Add the last token if any
if current_token:
    tokens.append(''.join(current_token))

print("Tokens:", tokens)

# Get class name
class_name = tokens[0] if tokens else ''
print("Class name:", class_name)

# Process parameters
if len(tokens) > 1:
    params = tokens[1:]
    print("Parameters:", params)
    
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            print(f"Key: {key}, Value: {value}")
            
            # Handle different value types
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]  # Remove quotes
                value = value.replace('_', ' ')  # Replace underscores
                value = value.replace('\\"', '"')  # Handle escaped quotes
                print(f"  -> String value: {value}")
            elif '.' in value:
                try:
                    value = float(value)
                    print(f"  -> Float value: {value}")
                except ValueError:
                    print(f"  -> Invalid float: {value}")
            else:
                try:
                    value = int(value)
                    print(f"  -> Integer value: {value}")
                except ValueError:
                    print(f"  -> Invalid integer: {value}")

print("\n--- Test 2: Multiple parameters ---")
args2 = 'Place city_id="0001" number_rooms=4 price_by_night=300 latitude=37.773972'

tokens2 = []
current_token2 = []
in_quotes2 = False

for char in args2:
    if char == '"':
        in_quotes2 = not in_quotes2
        current_token2.append(char)
    elif char == ' ' and not in_quotes2:
        if current_token2:
            tokens2.append(''.join(current_token2))
            current_token2 = []
    else:
        current_token2.append(char)

if current_token2:
    tokens2.append(''.join(current_token2))

print("Tokens:", tokens2)

for token in tokens2[1:]:
    if '=' in token:
        key, value = token.split('=', 1)
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            print(f"{key} = (str) {value}")
        elif '.' in value:
            try:
                value = float(value)
                print(f"{key} = (float) {value}")
            except ValueError:
                pass
        else:
            try:
                value = int(value)
                print(f"{key} = (int) {value}")
            except ValueError:
                pass
