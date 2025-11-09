import sys
import os

print("🧪 Testing Current Structure...")

# Add src to path
sys.path.insert(0, 'src')

try:
    # Test main app
    from app.main import main
    print("✅ Main app import successful")
    
    # Test auth module
    from modules.auth.auth_manager import auth_manager
    print("✅ Auth manager import successful")
    from modules.auth.auth_components import render_login_page
    print("✅ Auth components import successful")
    
    # Test assessment module
    from modules.assessment.framework import get_assessment_framework
    print("✅ Assessment framework import successful")
    from modules.assessment.engine import AssessmentEngine
    print("✅ Assessment engine import successful")
    
    # Test admin module
    from modules.admin.admin_components import render_admin_dashboard
    print("✅ Admin components import successful")
    
    print("🎉 ALL MODULES IMPORT SUCCESSFUL!")
    print("🚀 The application should run correctly!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Let's fix this import...")
except Exception as e:
    print(f"❌ Other error: {e}")

# Test if we can actually run the main function
try:
    print("\n🧪 Testing main function...")
    # We'll just import, not run, to avoid Streamlit issues
    from app.main import main
    print("✅ Main function can be imported")
except Exception as e:
    print(f"❌ Main function error: {e}")
