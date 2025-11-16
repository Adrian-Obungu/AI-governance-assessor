import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Complete Structure...")

try:
    # Test main app
    from src.app.main import main
    print("✅ Main app import successful")
    
    # Test database
    from modules.data.database_manager import db_manager
    print("✅ Database manager import successful")
    
    # Test auth
    from modules.auth.auth_manager import auth_manager
    print("✅ Auth manager import successful")
    from modules.auth.auth_components import render_auth_page
    print("✅ Auth components import successful")
    
    # Test admin
    from modules.admin.admin_components import render_admin_dashboard
    print("✅ Admin components import successful")
    
    # Test assessment
    from modules.assessment.scoring_engine import calculate_maturity_score
    print("✅ Scoring engine import successful")
    from modules.assessment.data_modules import load_assessment_data
    print("✅ Data modules import successful")
    
    # Test utils
    from modules.utils.report_generator import generate_assessment_report
    print("✅ Report generator import successful")
    from modules.utils.export_manager import export_user_data
    print("✅ Export manager import successful")
    
    print("🎉 ALL IMPORTS SUCCESSFUL!")
    print("🚀 The app should now work properly!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("We need to fix this import")
except Exception as e:
    print(f"❌ Other error: {e}")
