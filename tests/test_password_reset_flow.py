import sys
import os
import sqlite3
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modules.auth.auth_manager import AuthManager

DB_PATH = 'data/governance_assessments.db'
TEST_EMAIL = 'unit_test_user@example.com'
TEST_PASSWORD = 'InitialPass1!'
NEW_PASSWORD = 'NewPass2!'


def cleanup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (TEST_EMAIL,))
    cur.execute("DELETE FROM password_resets WHERE email=?", (TEST_EMAIL,))
    conn.commit()
    conn.close()


def test_password_reset_flow():
    cleanup()
    am = AuthManager()

    # create user
    ok, msg = am.create_user(TEST_EMAIL, TEST_PASSWORD, 'Unit Test', 'UnitOrg')
    assert ok, f"Failed to create user: {msg}"

    # authenticate with initial password
    user = am.authenticate(TEST_EMAIL, TEST_PASSWORD)
    assert user and user['email'] == TEST_EMAIL

    # create reset token
    token, err = am.create_password_reset_token(TEST_EMAIL)
    assert token is not None and err is None

    # verify token resolves to email
    email = am.verify_reset_token(token)
    assert email == TEST_EMAIL

    # reset password
    ok, reason = am.reset_password(token, NEW_PASSWORD)
    assert ok

    # authenticate with new password
    user2 = am.authenticate(TEST_EMAIL, NEW_PASSWORD)
    assert user2 and user2['email'] == TEST_EMAIL

    # cleanup
    cleanup()


def test_reset_with_invalid_token():
    am = AuthManager()
    ok, reason = am.reset_password('invalid-token-123', 'x')
    assert not ok
