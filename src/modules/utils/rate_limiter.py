"""
Rate limiting and brute-force protection utilities
"""
import sqlite3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting for authentication attempts"""
    
    DB_PATH = "data/governance_assessments.db"
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    ATTEMPT_WINDOW_MINUTES = 15
    
    @staticmethod
    def init_db():
        """Initialize rate limiting table"""
        try:
            conn = sqlite3.connect(RateLimiter.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifier TEXT NOT NULL,
                    attempt_count INTEGER DEFAULT 0,
                    first_attempt TIMESTAMP,
                    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    locked_until TIMESTAMP,
                    UNIQUE(identifier)
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rate_limits_identifier ON rate_limits(identifier)")
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing rate limiter: {str(e)}")
    
    @staticmethod
    def check_rate_limit(identifier: str) -> tuple[bool, str]:
        """
        Check if identifier (email or IP) has exceeded rate limit
        Returns: (is_allowed, message)
        """
        try:
            conn = sqlite3.connect(RateLimiter.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM rate_limits WHERE identifier = ?", (identifier,))
            record = cursor.fetchone()
            
            if not record:
                conn.close()
                return True, "OK"
            
            locked_until = record[5]
            if locked_until:
                locked_time = datetime.fromisoformat(locked_until)
                if datetime.now() < locked_time:
                    remaining = (locked_time - datetime.now()).total_seconds() / 60
                    conn.close()
                    return False, f"Account temporarily locked. Try again in {int(remaining)} minutes"
                else:
                    # Reset lockout
                    cursor.execute(
                        "UPDATE rate_limits SET locked_until = NULL, attempt_count = 0 WHERE identifier = ?",
                        (identifier,)
                    )
                    conn.commit()
            
            # Check if attempts window has expired
            first_attempt = datetime.fromisoformat(record[3])
            if datetime.now() > first_attempt + timedelta(minutes=RateLimiter.ATTEMPT_WINDOW_MINUTES):
                cursor.execute(
                    "UPDATE rate_limits SET attempt_count = 0, first_attempt = CURRENT_TIMESTAMP WHERE identifier = ?",
                    (identifier,)
                )
                conn.commit()
                conn.close()
                return True, "OK"
            
            conn.close()
            return True, "OK"
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {str(e)}")
            return True, "OK"
    
    @staticmethod
    def record_failed_attempt(identifier: str) -> bool:
        """Record a failed authentication attempt"""
        try:
            conn = sqlite3.connect(RateLimiter.DB_PATH)
            cursor = conn.cursor()
            
            # Get or create record
            cursor.execute("SELECT * FROM rate_limits WHERE identifier = ?", (identifier,))
            record = cursor.fetchone()
            
            if not record:
                cursor.execute("""
                    INSERT INTO rate_limits (identifier, attempt_count, first_attempt, last_attempt)
                    VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (identifier,))
            else:
                attempt_count = record[2] + 1
                
                # Check if should lock account
                if attempt_count >= RateLimiter.MAX_ATTEMPTS:
                    locked_until = (datetime.now() + timedelta(minutes=RateLimiter.LOCKOUT_DURATION_MINUTES)).isoformat()
                    cursor.execute(
                        "UPDATE rate_limits SET attempt_count = ?, last_attempt = CURRENT_TIMESTAMP, locked_until = ? WHERE identifier = ?",
                        (attempt_count, locked_until, identifier)
                    )
                    logger.warning(f"Rate limit exceeded for {identifier}. Account locked until {locked_until}")
                else:
                    cursor.execute(
                        "UPDATE rate_limits SET attempt_count = ?, last_attempt = CURRENT_TIMESTAMP WHERE identifier = ?",
                        (attempt_count, identifier)
                    )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error recording failed attempt: {str(e)}")
            return False
    
    @staticmethod
    def reset_attempts(identifier: str) -> bool:
        """Reset attempts for successful authentication"""
        try:
            conn = sqlite3.connect(RateLimiter.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE rate_limits SET attempt_count = 0, locked_until = NULL WHERE identifier = ?",
                (identifier,)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error resetting attempts: {str(e)}")
            return False
    
    @staticmethod
    def cleanup_expired_locks():
        """Clean up expired lockouts"""
        try:
            conn = sqlite3.connect(RateLimiter.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE rate_limits 
                SET locked_until = NULL, attempt_count = 0 
                WHERE locked_until IS NOT NULL AND locked_until < CURRENT_TIMESTAMP
            """)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up expired locks: {str(e)}")
            return False

# Initialize on import
RateLimiter.init_db()
