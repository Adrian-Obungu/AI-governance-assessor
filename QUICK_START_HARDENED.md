# Quick Start Guide – Running the Hardened App

**Latest Updates:** November 15, 2025  
All security hardening (Phases A–D) complete. This guide walks you through setup and testing the enhanced authentication flow.

---

## Prerequisites

```bash
# Python 3.10+
python --version

# Install dependencies
pip install -r requirements.txt
```

---

## Setup & First Run

### 1. Start the App
```bash
streamlit run src/app/main.py
```

The app will auto-initialize the database and create:
- `DemoOrg` organization
- `demo@demo.com` user (password: `demopassword`)
- All security tables (users, organizations, audit_logs, password_resets, password_reset_requests)

**Console Output Expected:**
```
Demo organization and demo user ensured.
Database initialized with schema and indexes
Streamlit app running at http://localhost:8501
```

---

## Testing the Authentication Flow

### Demo User (Quick Test)
**Email:** `demo@demo.com`  
**Password:** `demopassword`

1. Open http://localhost:8501
2. Click **Login** 
3. Enter credentials above
4. ✅ You should be logged in

---

## Testing Password Reset

### Scenario 1: Generate Reset Token (No SMTP Configured)

1. On the login page, click **Forgot password?**
2. Enter an email: `demo@demo.com`
3. Click **Get password reset token**
4. ✅ **Token displayed in app** (because SMTP not configured in dev mode)
5. Note the token

### Scenario 2: Use Reset Token to Change Password

1. On the login page, expand **"Have a reset token? Reset password here"**
2. Paste the token from step above
3. Enter a new password: `newpassword123`
4. Click **Reset password**
5. ✅ Success message shown
6. Log in with new password: `demo@demo.com` / `newpassword123`

---

## Testing Rate Limiting

Rate limit: **3 password reset requests per hour per email**

1. Click **Forgot password?**
2. Request 1: Enter `demo@demo.com` → Token generated ✅
3. Request 2: Click **Forgot password?** again → Token generated ✅
4. Request 3: Click **Forgot password?** again → Token generated ✅
5. Request 4: Click **Forgot password?** again → ❌ **"Rate limit exceeded"**
6. Wait 1 hour (or manually clear `password_reset_requests` table to test)
7. Try again → ✅ Token generated

---

## Testing Account Lockout

Account locks after **5 failed login attempts** for **30 minutes**

1. Open login page
2. Enter `demo@demo.com`
3. Enter wrong password 5 times
4. On 5th attempt: ❌ **"Account locked. Try again in 30 minutes"**
5. ✅ Cannot log in even with correct password until 30 min expires

---

## Run Unit Tests

```bash
# All password reset tests
pytest tests/test_password_reset_flow.py tests/test_password_reset_rate_limit.py -v

# Expected output
tests/test_password_reset_flow.py::test_create_reset_token PASSED
tests/test_password_reset_flow.py::test_verify_reset_token PASSED
tests/test_password_reset_rate_limit.py::test_rate_limit_password_resets PASSED
tests/test_password_reset_rate_limit.py::test_cleanup_expired_tokens PASSED

====== 4 passed in 1.89s ======
```

---

## Configure SMTP (Production)

To send password reset emails instead of displaying tokens:

### Step 1: Set Environment Variables

Create `.env` in project root:
```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@governance-assessor.com
```

### Step 2: Enable Less-Secure Apps (if using Gmail)
1. Go to https://myaccount.google.com/apppasswords
2. Create an app password for "Mail" / "Windows Computer"
3. Copy the 16-character password to `SMTP_PASSWORD` above

### Step 3: Restart App
```bash
streamlit run src/app/main.py
```

### Step 4: Test Email Delivery
1. **Forgot password?** for `demo@demo.com`
2. Check your email inbox for reset link/token
3. ✅ Email received

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "No module named 'modules'" | Run from project root: `cd /path/to/AI-governance-assessor` |
| Database locked error | Close all open connections; restart app |
| Email not sending | Check `.env` credentials; ensure SMTP port 587 is open |
| Reset token expired | Tokens expire in 60 minutes; generate a new one |
| Stuck in account lockout | Wait 30 minutes or manually clear `locked_until` in DB |

---

## Database Inspection (SQLite)

```bash
sqlite3 data/governance_assessments.db
```

### Check users
```sql
SELECT email, failed_login_attempts, locked_until FROM users;
```

### Check reset tokens
```sql
SELECT email, token, expires_at FROM password_resets;
```

### Check reset requests (for rate limiting)
```sql
SELECT email, requested_at FROM password_reset_requests;
```

### Manual cleanup (if needed)
```sql
-- Delete expired tokens
DELETE FROM password_resets WHERE expires_at < datetime('now');

-- Delete old requests (older than 7 days)
DELETE FROM password_reset_requests WHERE requested_at < datetime('now', '-7 days');
```

---

## File Locations

| Component | File |
|-----------|------|
| Authentication logic | `src/modules/auth/auth_manager.py` |
| Email sender | `src/modules/utils/email_sender.py` |
| Login UI | `src/modules/auth/auth_components.py` |
| Session state | `src/modules/utils/session_manager.py` |
| Multi-tenant queries | `src/modules/data/database_manager.py` |
| Database | `data/governance_assessments.db` |
| Tests | `tests/test_password_reset_*.py` |

---

## Next Steps

1. ✅ Test the app locally (follow scenarios above)
2. ✅ Run unit tests: `pytest tests/ -v`
3. ⏭️ Configure SMTP for your production email server
4. ⏭️ Deploy to staging environment
5. ⏭️ Set up scheduled cleanup task (call `cleanup_expired_tokens()` daily)
6. ⏭️ Move to production

---

## Support

For detailed deployment, hardening, and troubleshooting docs, see:
- **Deployment Readiness:** `DEPLOYMENT_READINESS_REPORT.md`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md` (if exists)

---

**Last Updated:** November 15, 2025  
**Status:** Ready for Testing & Staging Deployment
