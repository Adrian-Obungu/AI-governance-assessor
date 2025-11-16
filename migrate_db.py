#!/usr/bin/env python3
"""
Database migration script to add missing columns and reset for testing
"""
import os
import sqlite3
from datetime import datetime

db_path = "data/governance_assessments.db"

def migrate_database():
    """Migrate existing database to have all required columns"""
    if not os.path.exists(db_path):
        print(f"Database {db_path} does not exist. It will be created on first app run.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get existing columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Existing columns: {columns}")
        
        # Add missing columns
        missing_columns = {
            'locked_until': 'TIMESTAMP',
            'failed_login_attempts': 'INTEGER DEFAULT 0',
            'is_active': 'BOOLEAN DEFAULT 1',
            'created_at': "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            'updated_at': "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            'last_login': 'TIMESTAMP',
            'two_factor_enabled': 'BOOLEAN DEFAULT 0',
        }
        
        for col_name, col_type in missing_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                    print(f"✓ Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"✓ Column {col_name} already exists")
                    else:
                        print(f"✗ Error adding {col_name}: {e}")
        
        # Create audit_logs table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                resource_type TEXT,
                resource_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                details TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        print("✓ audit_logs table ready")
        
        # Create rate_limits table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT UNIQUE NOT NULL,
                attempt_count INTEGER DEFAULT 1,
                first_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                locked_until TIMESTAMP
            )
        """)
        print("✓ rate_limits table ready")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_database():
    """Delete the database to start fresh"""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Deleted {db_path}")
        print("Database will be recreated with fresh schema on next app run")
        return True
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        print("Resetting database...")
        reset_database()
    else:
        print("Running database migration...\n")
        migrate_database()
