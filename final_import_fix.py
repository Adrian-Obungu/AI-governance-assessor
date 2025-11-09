import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix import patterns for the new structure
    fixes = [
        # Remove problematic imports from __init__.py files
        (r'from \.scoring_engine import \*', 'from .scoring_engine import calculate_maturity_score, get_maturity_level'),
        (r'from \.report_generator import \*', 'from .report_generator import generate_assessment_report, export_to_json'),
        
        # Ensure proper relative imports
        (r'from scoring_engine', 'from .scoring_engine'),
        (r'from report_generator', 'from .report_generator'),
        (r'from data_modules', 'from .data_modules'),
        (r'from database_manager', 'from ..data.database_manager'),
        (r'from auth_manager', 'from ..auth.auth_manager'),
    ]
    
    new_content = content
    for pattern, replacement in fixes:
        new_content = re.sub(pattern, replacement, new_content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {filepath}")

# Fix all __init__.py files
init_files = [
    'src/modules/__init__.py',
    'src/modules/assessment/__init__.py', 
    'src/modules/utils/__init__.py',
    'src/modules/auth/__init__.py',
    'src/modules/admin/__init__.py',
    'src/modules/data/__init__.py'
]

for filepath in init_files:
    if os.path.exists(filepath):
        fix_file(filepath)

print("Import fixes completed!")
