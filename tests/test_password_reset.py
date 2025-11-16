import sys
import os
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modules.auth.auth_manager import AuthManager


def setup_function():
    # Ensure a clean test DB copy for tests
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'governance_assessments.db'))
    # Use the same DB; AuthManager uses it and is idempotent for our small tests


def test_create_and_use_password_reset():
    am = AuthManager()
    email = 'temp_reset_user@example.com'

    # Clean existing user
    conn = sqlite3.connect(am.db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()

    # Create user
    success, msg = am.create_user(email, 'ResetPass123!', 'Reset User', 'DemoOrg')
    assert success, f"create_user failed: {msg}"

    # Create token
    token, err = am.create_password_reset_token(email)
    assert token is not None and err is None

    # Verify token resolves to email
    linked = am.verify_reset_token(token)
    assert linked == email

    # Reset password
    ok, reason = am.reset_password(token, 'NewStrongPass1!')
    assert ok and reason is None

    # Authenticate with new password
    user = am.authenticate(email, 'NewStrongPass1!')
    assert user is not None

    # Cleanup
    conn = sqlite3.connect(am.db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()
