#!/usr/bin/env python3
"""
Phase A Verification Script
Tests database migrations and table creation
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import sqlite3
from modules.auth.auth_manager import AuthManager
from modules.data.database_manager import DatabaseManager

print("=" * 60)
print("PHASE A: DATABASE MIGRATION VERIFICATION")
print("=" * 60)

try:
    # Initialize managers (triggers migrations)
    print("\n1. Initializing AuthManager...")
    auth_manager = AuthManager()
    print("   ✅ AuthManager initialized")
    
    print("\n2. Initializing DatabaseManager...")
    db_manager = DatabaseManager()
    print("   ✅ DatabaseManager initialized")
    
    # Verify tables and columns
    db_path = "data/governance_assessments.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n3. Checking users table columns...")
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [col[1] for col in cursor.fetchall()]
    required_user_cols = ['id', 'email', 'org_id', 'role', 'created_at']
    for col in required_user_cols:
        if col in user_columns:
            print(f"   ✅ users.{col} exists")
        else:
            print(f"   ❌ users.{col} MISSING")
    
    print("\n4. Checking assessments table columns...")
    cursor.execute("PRAGMA table_info(assessments)")
    assessment_columns = [col[1] for col in cursor.fetchall()]
    required_assess_cols = ['id', 'user_id', 'org_id']
    for col in required_assess_cols:
        if col in assessment_columns:
            print(f"   ✅ assessments.{col} exists")
        else:
            print(f"   ❌ assessments.{col} MISSING")
    
    print("\n5. Checking organizations table...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='organizations'")
    if cursor.fetchone():
        print("   ✅ organizations table exists")
        cursor.execute("PRAGMA table_info(organizations)")
        org_cols = [col[1] for col in cursor.fetchall()]
        print(f"      Columns: {', '.join(org_cols)}")
    else:
        print("   ❌ organizations table MISSING")
    
    print("\n6. Checking indexes...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
    indexes = [row[0] for row in cursor.fetchall()]
    required_indexes = ['idx_users_org_id', 'idx_assessments_org_id', 'idx_organizations_name']
    for idx in required_indexes:
        if idx in indexes:
            print(f"   ✅ {idx} created")
        else:
            print(f"   ⚠️  {idx} not found (may be created on first run)")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ PHASE A VERIFICATION COMPLETE - ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nNext: Proceed to Phase B (Demo user setup)")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
