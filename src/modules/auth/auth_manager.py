import sqlite3
import bcrypt
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        self.db_path = "data/governance_assessments.db"
        self._init_db()
        # DEPRECATED: Demo users removed for security. Use register endpoint.
        self.demo_users = {}
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                organization TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                last_login TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP,
                two_factor_enabled BOOLEAN DEFAULT 0
            )
        """)
        
        # Create audit log table
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
        
        # Create index for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_logs(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
        
        conn.commit()
        conn.close()
        logger.info("Database initialized with schema and indexes")
    
    def create_user(self, email, password, full_name, organization, role="user"):
        if self.get_user(email):
            return False, "Email already registered"
        
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash, full_name, organization, role) VALUES (?, ?, ?, ?, ?)",
                (email, password_hash, full_name, organization, role)
            )
            conn.commit()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "User already exists"
        finally:
            conn.close()
    
    def authenticate(self, email, password):
        """Authenticate user with brute-force protection"""
        # Demo users removed - use registration
        
        # Database users
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if account is locked
        cursor.execute("SELECT locked_until FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        
        if result and result[0]:
            from datetime import datetime
            locked_until = datetime.fromisoformat(result[0])
            if datetime.now() < locked_until:
                logger.warning(f"Login attempt on locked account: {email}")
                conn.close()
                return None
        
        # Get user credentials
        cursor.execute("SELECT id, email, password_hash, full_name, organization, role, failed_login_attempts FROM users WHERE email=? AND is_active=1", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user[2].encode()):
            # Login successful - reset failed attempts
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET failed_login_attempts=0, last_login=CURRENT_TIMESTAMP WHERE id=?", (user[0],))
            conn.commit()
            conn.close()
            
            logger.info(f"Successful authentication for user: {email}")
            
            return {
                "user_id": user[0],
                "email": user[1],
                "full_name": user[3],
                "organization": user[4],
                "role": user[5],
                "limitations": {}
            }
        
        # Login failed - increment failed attempts
        if user:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT failed_login_attempts FROM users WHERE id=?", (user[0],))
            attempts = cursor.fetchone()[0] + 1
            
            # Lock account after 5 failed attempts
            if attempts >= 5:
                from datetime import datetime, timedelta
                locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
                cursor.execute("UPDATE users SET failed_login_attempts=?, locked_until=? WHERE id=?", (attempts, locked_until, user[0]))
                logger.warning(f"Account locked after 5 failed attempts: {email}")
            else:
                cursor.execute("UPDATE users SET failed_login_attempts=? WHERE id=?", (attempts, user[0]))
            
            conn.commit()
            conn.close()
            logger.warning(f"Failed authentication attempt for user: {email} (attempt #{attempts})")
        
        return None
    
    def get_user(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        return bool(user)

auth_manager = AuthManager()
