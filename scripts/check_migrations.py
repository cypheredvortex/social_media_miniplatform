import os
import sys

# Check migration files
for root, dirs, files in os.walk('apps'):
    for file in files:
        if file.endswith('0001_initial.py'):
            filepath = os.path.join(root, file)
            print(f"\nChecking: {filepath}")
            with open(filepath, 'r') as f:
                content = f.read()
                if 'ObjectIdField' in content:
                    print("  ✓ Contains ObjectIdField")
                elif 'AutoField' in content:
                    print("  ✗ Contains AutoField (WRONG!)")
                else:
                    print("  ? Unknown field type")