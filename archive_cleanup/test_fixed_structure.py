import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Fixed Structure...")

try:
    # Test main app import
    from src.app.main import main
    print("✅ Main app import successful")
    
    # Test database manager
    from modules.data.database_manager import db_manager
    print("✅ Database manager import successful")
    
    # Test auth manager  
    from modules.auth.auth_manager import auth_manager
    print("✅ Auth manager import successful")
    
    # Test auth components
    from modules.auth.auth_components import render_auth_page
    print("✅ Auth components import successful")
    
    # Test admin components
    from modules.admin.admin_components import render_admin_dashboard
    print("✅ Admin components import successful")
    
    # Test scoring engine
    from modules.assessment.scoring_engine import calculate_maturity_score
    print("✅ Scoring engine import successful")
    
    # Test settings
    from src.app.config.settings import DATABASE_PATH, FRAMEWORK_PATH
    print("✅ Settings import successful")
    print(f"   Database path: {DATABASE_PATH}")
    print(f"   Database exists: {DATABASE_PATH.exists()}")
    
    print("🎉 All imports successful! The app should run now.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run the import fixer scripts again.")
except Exception as e:
    print(f"❌ Other error: {e}")
