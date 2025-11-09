import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database configuration
DATABASE_PATH = BASE_DIR / "governance_assessments.db"  # Temporary - file is at root

# Upload directories
EVIDENCE_UPLOAD_PATH = BASE_DIR / "evidence_uploads"
SESSIONS_PATH = BASE_DIR / "saved_sessions"

# Framework paths
FRAMEWORK_PATH = BASE_DIR / "src" / "modules" / "assessment" / "frameworks" / "nist_rmf_enhanced.json"

# App settings
APP_NAME = "AI Governance Pro"
APP_VERSION = "3.2"

print(f"Database path: {DATABASE_PATH}")
print(f"Database exists: {DATABASE_PATH.exists()}")
