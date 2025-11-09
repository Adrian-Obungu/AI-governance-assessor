import re

# Read the main.py file
with open('src/app/main.py', 'r') as f:
    content = f.read()

# Fix the import patterns
fixes = [
    (r'from src\.modules\.database_manager', 'from modules.data.database_manager'),
    (r'from src\.modules\.auth_manager', 'from modules.auth.auth_manager'),
    (r'from src\.modules\.auth_components', 'from modules.auth.auth_components'),
    (r'from src\.modules\.admin_components', 'from modules.admin.admin_components'),
    (r'from src\.modules\.scoring_engine', 'from modules.assessment.scoring_engine'),
]

new_content = content
for old_pattern, new_pattern in fixes:
    new_content = re.sub(old_pattern, new_pattern, new_content)

# Write the fixed content back
with open('src/app/main.py', 'w') as f:
    f.write(new_content)

print("✅ Fixed imports in main.py")
