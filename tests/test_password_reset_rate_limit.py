import os
import tempfile
import sqlite3
import time
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from modules.auth.auth_manager import AuthManager


def test_rate_limit_password_resets():
    # Use a temporary database file
    tmp_db = tempfile.NamedTemporaryFile(delete=False)
    tmp_db_path = tmp_db.name
    tmp_db.close()

    # Patch auth manager to use temp DB
    am = AuthManager()
    am.db_path = tmp_db_path
    am._init_db()

    # Create a user to test with
    am.create_user('ratelimit@example.com', 'password123', 'Rate Limit', 'TestOrg')

    # First three requests should succeed
    for i in range(3):
        token, err = am.create_password_reset_token('ratelimit@example.com')
        assert token is not None and err is None

    # Fourth request within window should be rate-limited
    token, err = am.create_password_reset_token('ratelimit@example.com')
    assert token is None and err == 'rate_limited'

    # Advance time by clearing old requests (simulate by deleting rows older than window)
    conn = sqlite3.connect(tmp_db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM password_reset_requests")
    conn.commit()
    conn.close()

    # Now request should succeed again
    token, err = am.create_password_reset_token('ratelimit@example.com')
    assert token is not None and err is None

    os.unlink(tmp_db_path)


def test_cleanup_expired_tokens():
    # Use a temporary database file
    tmp_db = tempfile.NamedTemporaryFile(delete=False)
    tmp_db_path = tmp_db.name
    tmp_db.close()

    # Patch auth manager to use temp DB
    am = AuthManager()
    am.db_path = tmp_db_path
    am._init_db()

    # Create a user and generate a token
    am.create_user('cleanup@example.com', 'password123', 'Cleanup Test', 'TestOrg')
    token, _ = am.create_password_reset_token('cleanup@example.com')

    # Verify token exists
    conn = sqlite3.connect(tmp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM password_resets WHERE token=?", (token,))
    assert cursor.fetchone()[0] == 1

    # Manually expire the token by setting expires_at to the past
    past = (datetime.now() - timedelta(hours=2)).isoformat()
    cursor.execute("UPDATE password_resets SET expires_at=? WHERE token=?", (past, token))
    conn.commit()

    # Also add old request records
    old_date = (datetime.now() - timedelta(days=8)).isoformat()
    cursor.execute("INSERT INTO password_reset_requests (email, requested_at) VALUES (?, ?)", ('cleanup@example.com', old_date))
    conn.commit()

    # Count before cleanup
    cursor.execute("SELECT COUNT(*) FROM password_reset_requests")
    before_requests = cursor.fetchone()[0]
    assert before_requests >= 1

    conn.close()

    # Run cleanup
    am.cleanup_expired_tokens()

    # Verify expired token was deleted
    conn = sqlite3.connect(tmp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM password_resets WHERE token=?", (token,))
    assert cursor.fetchone()[0] == 0

    # Verify old request records were deleted
    cursor.execute("SELECT COUNT(*) FROM password_reset_requests WHERE requested_at=?", (old_date,))
    assert cursor.fetchone()[0] == 0

    conn.close()
    os.unlink(tmp_db_path)
