import os
import re

def update_imports(filepath):
    """Update import paths in a file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix import patterns
    fixes = [
        # Ensure proper relative imports
        (r'from modules\.', 'from .'),
        (r'from auth\.', 'from .'),
        (r'from assessment\.', 'from .'),
        (r'from admin\.', 'from .'),
        (r'from data\.', 'from .'),
        (r'from utils\.', 'from .'),
    ]
    
    new_content = content
    for pattern, replacement in fixes:
        new_content = re.sub(pattern, replacement, new_content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")

# Update module __init__.py files
init_files = [
    'src/modules/auth/__init__.py',
    'src/modules/assessment/__init__.py',
    'src/modules/admin/__init__.py', 
    'src/modules/data/__init__.py',
    'src/modules/utils/__init__.py'
]

for filepath in init_files:
    if os.path.exists(filepath):
        update_imports(filepath)

print("Import paths updated!")
