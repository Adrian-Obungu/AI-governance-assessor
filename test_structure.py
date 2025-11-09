import sys
import os

# Add src to path
sys.path.insert(0, 'src')

try:
    # Test main app import
    from app.main import main
    print("✅ Main app import successful")
    
    # Test database manager
    from modules.data.database_manager import db_manager
    print("✅ Database manager import successful")
    
    # Test auth manager  
    from modules.auth.auth_manager import auth_manager
    print("✅ Auth manager import successful")
    
    # Test settings
    from app.config.settings import DATABASE_PATH, FRAMEWORK_PATH
    print(f"✅ Settings import successful")
    print(f"   Database path: {DATABASE_PATH}")
    print(f"   Database exists: {DATABASE_PATH.exists()}")
    print(f"   Framework path: {FRAMEWORK_PATH}")
    print(f"   Framework exists: {FRAMEWORK_PATH.exists()}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
