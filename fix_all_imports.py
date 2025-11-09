import os
import re

def fix_imports_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix import patterns
    fixes = [
        # Remove src. prefix from all imports
        (r'from src\.modules\.', 'from modules.'),
        (r'import src\.modules\.', 'import modules.'),
        (r'from src\.app\.', 'from app.'),
        (r'import src\.app\.', 'import app.'),
        
        # Fix specific module imports to new structure
        (r'from modules\.database_manager', 'from modules.data.database_manager'),
        (r'from modules\.auth_manager', 'from modules.auth.auth_manager'),
        (r'from modules\.auth_components', 'from modules.auth.auth_components'),
        (r'from modules\.admin_components', 'from modules.admin.admin_components'),
        (r'from modules\.scoring_engine', 'from modules.assessment.scoring_engine'),
        (r'from modules\.data_modules', 'from modules.assessment.data_modules'),
        (r'from modules\.user_data_manager', 'from modules.data.user_data_manager'),
        (r'from modules\.evidence_manager', 'from modules.data.evidence_manager'),
        (r'from modules\.export_manager', 'from modules.utils.export_manager'),
        (r'from modules\.navigation_manager', 'from modules.utils.navigation_manager'),
        (r'from modules\.report_generator', 'from modules.utils.report_generator'),
        (r'from modules\.session_manager', 'from modules.utils.session_manager'),
        (r'from modules\.analytics_dashboard', 'from modules.utils.analytics_dashboard'),
    ]
    
    new_content = content
    for pattern, replacement in fixes:
        new_content = re.sub(pattern, replacement, new_content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"✅ Fixed: {filepath}")

# Fix all Python files in the src directory
for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            fix_imports_in_file(filepath)

print("🎉 All imports fixed!")
