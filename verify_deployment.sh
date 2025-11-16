#!/bin/bash
# Deployment Verification Script

echo "🔍 DEPLOYMENT VERIFICATION"
echo "=========================="

# Check critical files
echo "1. Checking critical files..."
CRITICAL_FILES=(
    "src/app/main.py"
    "src/modules/auth/auth_manager.py" 
    "src/modules/auth/auth_components.py"
    "src/modules/assessment/framework.py"
    "src/modules/assessment/engine.py"
    "src/modules/utils/navigation_manager.py"
    "src/modules/utils/analytics_dashboard.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING"
    fi
done

# Test Python imports
echo ""
echo "2. Testing Python imports..."
python3 -c "
import sys
import os
sys.path.append('src')

try:
    from modules.auth.auth_manager import auth_manager
    print('✅ auth_manager import successful')
    
    from modules.auth.auth_components import render_login_page, render_registration_page  
    print('✅ auth_components import successful')
    
    from modules.assessment.framework import get_assessment_framework
    print('✅ framework import successful')
    
    from modules.assessment.engine import render_assessment_ui, apply_user_limitations
    print('✅ engine import successful')
    
    from modules.utils.navigation_manager import NavigationManager
    print('✅ navigation_manager import successful')
    
    from modules.utils.analytics_dashboard import display_results_dashboard
    print('✅ analytics_dashboard import successful')
    
    print('🎉 ALL IMPORTS SUCCESSFUL')
    
except Exception as e:
    print(f'❌ Import error: {e}')
    import traceback
    traceback.print_exc()
"

# Test demo functionality
echo ""
echo "3. Testing demo functionality..."
python3 -c "
import sys
sys.path.append('src')

try:
    from modules.auth.auth_manager import auth_manager
    user = auth_manager.authenticate('user@demo.com', 'demo')
    if user and user.get('limitations', {}).get('max_questions') == 10:
        print('✅ Demo user: 10-question limit enforced')
    else:
        print('❌ Demo user limitations issue')
        
    # Test framework loading
    from modules.assessment.framework import get_assessment_framework
    framework = get_assessment_framework()
    if framework and len(framework) == 5:
        print('✅ Framework: 5 domains loaded')
    else:
        print('❌ Framework loading issue')
        
except Exception as e:
    print(f'❌ Functionality test error: {e}')
"

echo ""
echo "🚀 VERIFICATION COMPLETE"
