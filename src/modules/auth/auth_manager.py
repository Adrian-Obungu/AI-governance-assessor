import sqlite3
import bcrypt
import logging

logger = logging.getLogger(__name__)

# Rate limit configuration for password reset requests
RATE_LIMIT_WINDOW_MINUTES = 60
RATE_LIMIT_MAX_REQUESTS = 3

class AuthManager:
    def __init__(self):
        self.db_path = "data/governance_assessments.db"
        self._init_db()
        self.ensure_demo_user_exists()
        # DEPRECATED: Demo users removed for security. Use register endpoint.
        self.demo_users = {}
    
    def ensure_demo_user_exists(self):
        """Create demo organization and demo user if not present."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create demo organization if not exists
        cursor.execute("SELECT id FROM organizations WHERE name=?", ("DemoOrg",))
        org = cursor.fetchone()
        if not org:
            cursor.execute("INSERT INTO organizations (name, industry, size, region) VALUES (?, ?, ?, ?)",
                           ("DemoOrg", "Technology", "Small", "Global"))
            conn.commit()
            cursor.execute("SELECT id FROM organizations WHERE name=?", ("DemoOrg",))
            org = cursor.fetchone()
        org_id = org[0]
        # Create demo user if not exists
        cursor.execute("SELECT id FROM users WHERE email=?", ("demo@demo.com",))
        user = cursor.fetchone()
        if not user:
            password_hash = bcrypt.hashpw("demopassword".encode(), bcrypt.gensalt())
            cursor.execute("INSERT INTO users (email, password_hash, full_name, organization, role, org_id, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           ("demo@demo.com", sqlite3.Binary(password_hash), "Demo User", "DemoOrg", "demo", org_id, 1))
            conn.commit()
        conn.close()
        logger.info("Demo organization and demo user ensured.")
    
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
        
        # Database migration: Add missing columns if they don't exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add missing security columns
        if 'locked_until' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN locked_until TIMESTAMP")
            logger.info("Added locked_until column to users table")
        if 'failed_login_attempts' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0")
            logger.info("Added failed_login_attempts column to users table")
        if 'is_active' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
            logger.info("Added is_active column to users table")
        if 'created_at' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP")
            logger.info("Added created_at column to users table")
        if 'updated_at' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP")
            logger.info("Added updated_at column to users table")
        if 'last_login' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
            logger.info("Added last_login column to users table")
        if 'two_factor_enabled' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN two_factor_enabled BOOLEAN DEFAULT 0")
            logger.info("Added two_factor_enabled column to users table")
        if 'org_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN org_id INTEGER")
            logger.info("Added org_id column to users table")
        
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
        
        # Create organizations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                industry TEXT,
                size TEXT,
                region TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_org_id ON users(org_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_logs(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_organizations_name ON organizations(name)")
        # Password resets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Password reset requests table (for rate limiting)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_prr_email_requested_at ON password_reset_requests(email, requested_at)")
        
        conn.commit()
        conn.close()
        logger.info("Database initialized with schema and indexes")
    
    def create_user(self, email, password, full_name, organization, role="user"):
        if self.get_user(email):
            return False, "Email already registered"
        
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash, full_name, organization, role) VALUES (?, ?, ?, ?, ?)",
                (email, sqlite3.Binary(password_hash), full_name, organization, role)
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
        
        if user:
            # Normalize stored password hash to bytes for bcrypt
            stored_hash = user[2]
            if isinstance(stored_hash, str):
                hashed_bytes = stored_hash.encode('utf-8')
            elif isinstance(stored_hash, memoryview):
                hashed_bytes = stored_hash.tobytes()
            elif isinstance(stored_hash, bytes):
                hashed_bytes = stored_hash
            else:
                try:
                    hashed_bytes = bytes(stored_hash)
                except Exception:
                    logger.error(f"Unrecognized password hash type for user {email}: {type(stored_hash)}")
                    conn.close()
                    return None

            if bcrypt.checkpw(password.encode(), hashed_bytes):
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

    def create_password_reset_token(self, email, expiry_minutes=60):
        """Create a password reset token for the specified email. Returns token or (None, 'not_found'|'rate_limited')."""
        if not self.get_user(email):
            return None, 'not_found'

        from datetime import datetime, timedelta
        now = datetime.now()
        window_start = (now - timedelta(minutes=RATE_LIMIT_WINDOW_MINUTES)).isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Count requests within the rate-limit window
        cursor.execute("SELECT COUNT(*) FROM password_reset_requests WHERE email=? AND requested_at>=?", (email, window_start))
        row = cursor.fetchone()
        recent_count = row[0] if row else 0
        if recent_count >= RATE_LIMIT_MAX_REQUESTS:
            conn.close()
            logger.warning(f"Password reset rate limit exceeded for {email}: {recent_count} requests in window")
            return None, 'rate_limited'

        # Record this request
        cursor.execute("INSERT INTO password_reset_requests (email, requested_at) VALUES (?, ?)", (email, now.isoformat()))

        import secrets
        token = secrets.token_urlsafe(32)
        expires_at = (now + timedelta(minutes=expiry_minutes)).isoformat()

        cursor.execute("INSERT INTO password_resets (email, token, expires_at) VALUES (?, ?, ?)", (email, token, expires_at))
        conn.commit()
        conn.close()

        # Attempt to send reset email; if SMTP not configured, caller can still display token
        try:
            try:
                from modules.utils.email_sender import send_reset_email
            except Exception:
                from src.modules.utils.email_sender import send_reset_email

            sent, err = send_reset_email(email, token)
            if not sent:
                logger.warning(f"Password reset token created but failed to send email: {err}")
            return token, None
        except Exception:
            logger.exception("Error while attempting to send reset email; falling back to returning token")
            return token, None

    def verify_reset_token(self, token):
        """Verify token and return associated email or None if invalid/expired."""
        from datetime import datetime
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT email, expires_at FROM password_resets WHERE token=?", (token,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        email, expires_at = row
        try:
            if datetime.fromisoformat(expires_at) < datetime.now():
                return None
        except Exception:
            return None
        return email

    def reset_password(self, token, new_password):
        """Reset password using token. Returns (True, None) on success or (False, reason)."""
        email = self.verify_reset_token(token)
        if not email:
            return False, 'invalid_or_expired'

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash=? WHERE email=?", (sqlite3.Binary(new_hash), email))
        cursor.execute("DELETE FROM password_resets WHERE token=?", (token,))
        conn.commit()
        conn.close()
        return True, None

    def is_account_locked(self, email):
        """Return True if account is currently locked, else False."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT locked_until FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        conn.close()
        if not row or not row[0]:
            return False
        from datetime import datetime
        try:
            locked_until = datetime.fromisoformat(row[0])
            return datetime.now() < locked_until
        except Exception:
            return False

    def cleanup_expired_tokens(self):
        """Remove expired password reset tokens and old reset request records."""
        from datetime import datetime, timedelta
        now = datetime.now().isoformat()
        # Remove expired tokens (older than expiry_at)
        old_window = (datetime.fromisoformat(now) - timedelta(days=7)).isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Delete expired password reset tokens
        cursor.execute("DELETE FROM password_resets WHERE expires_at < ?", (now,))
        deleted_tokens = cursor.rowcount
        # Delete old reset request records (older than 7 days)
        cursor.execute("DELETE FROM password_reset_requests WHERE requested_at < ?", (old_window,))
        deleted_requests = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted_tokens > 0 or deleted_requests > 0:
            logger.info(f"Cleanup: removed {deleted_tokens} expired tokens and {deleted_requests} old request records")

auth_manager = AuthManager()
