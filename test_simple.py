import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Simple Imports...")

try:
    from src.app.main import main
    print("✅ Main app import successful")
    
    from modules.auth.auth_components import render_auth_page
    print("✅ Auth components import successful")
    
    from modules.auth.auth_manager import auth_manager
    print("✅ Auth manager import successful")
    
    from modules.data.database_manager import db_manager
    print("✅ Database manager import successful")
    
    from modules.admin.admin_components import render_admin_dashboard
    print("✅ Admin components import successful")
    
    print("🎉 All basic imports working!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
