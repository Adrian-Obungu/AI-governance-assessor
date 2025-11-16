# 🔍 PRIORITY 1 IMPLEMENTATION - DISCOVERY REPORT

**Date:** November 15, 2025  
**Phase:** Pre-Implementation Analysis  
**Risk Level:** Low-Medium with Safe Approach

---

## 📊 CURRENT STATE ANALYSIS

### Database Schema Status

#### ✅ Users Table (READY)
```sql
id, email, password_hash, full_name, organization, role
created_at, updated_at, is_active, last_login
failed_login_attempts, locked_until, two_factor_enabled
```
- ✅ 13 columns - all needed fields present
- ✅ Foreign keys in place
- ✅ Indexes created
- ⚠️ MISSING: `org_id` column (needed for multi-tenant isolation)

#### ✅ Assessments Table (READY)
```sql
id, user_id, assessment_name, framework_version
overall_score, overall_maturity, completion_percentage
created_at, updated_at, submitted_at, status
```
- ✅ Properly structured
- ✅ Has user_id for linking
- ⚠️ MISSING: `org_id` column (for multi-tenant queries)

#### ❓ Organizations Table (UNKNOWN)
- Not found in `database_manager.py`
- Not found in `auth_manager.py`
- **ACTION REQUIRED:** Need to create this table

---

## 🛠️ SPECIFIC IMPLEMENTATION TASKS

### TASK 1: Add org_id Columns to Users Table

**File:** `src/modules/auth/auth_manager.py`

**Current _init_db() creates:**
```python
users TABLE # With 13 columns but NO org_id
```

**Need to add in migration section:**
```python
# After checking for two_factor_enabled:
if 'org_id' not in columns:
    cursor.execute("""
        ALTER TABLE users ADD COLUMN org_id INTEGER
    """)
    logger.info("Added org_id column to users table")
```

**Location:** After line 57 in auth_manager.py (after two_factor_enabled check)

**Why:** Without org_id on users, we can't efficiently filter assessments by organization

**Risk:** 🟢 LOW - Additive column migration, safe for existing data

---

### TASK 2: Add org_id Column to Assessments Table

**File:** `src/modules/data/database_manager.py`

**Current _init_assessment_schema() creates:**
```python
assessments TABLE # With user_id but NO org_id
```

**Need to add in migration section:**
```python
# After creating assessment_responses table:
cursor.execute("PRAGMA table_info(assessments)")
assessment_columns = [col[1] for col in cursor.fetchall()]

if 'org_id' not in assessment_columns:
    cursor.execute("""
        ALTER TABLE assessments ADD COLUMN org_id INTEGER
    """)
    logger.info("Added org_id column to assessments table")
```

**Location:** After line 50 in database_manager.py (after domain_scores creation)

**Why:** Allows filtering assessments by organization instead of just user_id

**Risk:** 🟢 LOW - Additive column migration

---

### TASK 3: Create Organizations Table

**File:** `src/modules/auth/auth_manager.py`

**Add to _init_db() method:**
```python
# Add after audit_logs table creation:
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
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_organizations_name 
    ON organizations(name)
""")
logger.info("Organizations table created")
```

**Location:** Around line 70 in auth_manager.py

**Why:** Provides structure for multi-tenant data organization

**Risk:** 🟢 LOW - `CREATE TABLE IF NOT EXISTS` is idempotent

---

### TASK 4: Add Demo User Auto-Creation

**File:** `src/modules/auth/auth_manager.py`

**Add new method:**
```python
def ensure_demo_user_exists(self):
    """
    Create demo user on first run if doesn't exist.
    Safe to call multiple times (idempotent).
    """
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    # Check if demo user exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@example.com",))
    if cursor.fetchone():
        return  # Already exists
    
    try:
        # Create demo organization first
        cursor.execute("SELECT id FROM organizations WHERE name = ?", ("Demo Organization",))
        org_result = cursor.fetchone()
        
        if org_result:
            demo_org_id = org_result[0]
        else:
            cursor.execute("""
                INSERT INTO organizations (name, industry, size, region)
                VALUES (?, ?, ?, ?)
            """, ("Demo Organization", "Technology", "1-50", "Global"))
            demo_org_id = cursor.lastrowid
        
        # Create demo user
        password_hash = bcrypt.hashpw(b"demo", bcrypt.gensalt()).decode()
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, 
                              organization, org_id, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("demo@example.com", password_hash, "Demo User", 
              "Demo Organization", demo_org_id, "demo", 1))
        
        conn.commit()
        logger.info("Demo user created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create demo user: {e}")
    finally:
        conn.close()
```

**Call from:** `__init__()` method after `_init_db()`
```python
def __init__(self):
    self.db_path = "data/governance_assessments.db"
    self._init_db()
    self.ensure_demo_user_exists()  # ADD THIS
```

**Location:** Line 11 in auth_manager.py (add ensure_demo_user_exists() call)

**Why:** Automatically sets up demo account without manual creation

**Risk:** 🟢 LOW - Checks for existence before creating, safe to call repeatedly

---

### TASK 5: Restore Demo Login Button

**File:** `src/modules/auth/auth_components.py`

**Add after current login form (around line 325):**
```python
# Demo user option
st.markdown("---")
st.subheader("🎬 Want to Try First?")

col1, col2 = st.columns(2)
with col1:
    st.info("Demo account limited to 10 questions")
with col2:
    if st.button("🎯 Demo Login", use_container_width=True, type="secondary"):
        user = auth_manager.authenticate("demo@example.com", "demo")
        if user:
            login_user(user)
            st.success("Welcome to demo! You can answer up to 10 questions.")
        else:
            st.error("Demo user not available")
```

**Location:** After manual login form, before registration section

**Why:** Gives users option to try demo before registering

**Risk:** 🟢 LOW - Additive UI, doesn't affect existing flows

---

### TASK 6: Add Multi-Tenant Query Functions

**File:** `src/modules/data/database_manager.py`

**Add new method:**
```python
def get_user_assessments_isolated(self, user_id, org_id):
    """
    Get user's assessments with organization isolation.
    Returns empty list if org_id doesn't match user's organization.
    """
    try:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First verify user belongs to org
        cursor.execute("SELECT org_id FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        
        if not result or result[0] != org_id:
            logger.warning(f"Unauthorized access attempt: user {user_id} accessing org {org_id}")
            conn.close()
            return []
        
        # Then get assessments with org filter
        cursor.execute("""
            SELECT * FROM assessments 
            WHERE user_id=? AND org_id=?
            ORDER BY created_at DESC
        """, (user_id, org_id))
        
        assessments = cursor.fetchall()
        conn.close()
        return assessments or []
        
    except Exception as e:
        logger.error(f"Error retrieving isolated assessments: {str(e)}")
        return []
```

**Also add:**
```python
def get_assessment_by_id_isolated(self, assessment_id, user_id, org_id):
    """
    Get specific assessment with organization isolation.
    Validates both user and organization ownership.
    """
    try:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify access
        cursor.execute("""
            SELECT a.* FROM assessments a
            JOIN users u ON a.user_id = u.id
            WHERE a.id=? AND a.user_id=? AND a.org_id=? AND u.org_id=?
        """, (assessment_id, user_id, org_id, org_id))
        
        assessment = cursor.fetchone()
        
        if not assessment:
            logger.warning(f"Unauthorized assessment access: user {user_id}, assessment {assessment_id}")
            conn.close()
            return None
        
        # Get domain scores and responses
        cursor.execute("""
            SELECT * FROM domain_scores WHERE assessment_id=?
        """, (assessment_id,))
        domain_scores = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM assessment_responses WHERE assessment_id=?
        """, (assessment_id,))
        responses = cursor.fetchall()
        
        conn.close()
        
        return {
            'assessment': assessment,
            'domain_scores': domain_scores,
            'responses': responses
        }
        
    except Exception as e:
        logger.error(f"Error retrieving isolated assessment: {str(e)}")
        return None
```

**Location:** Add after existing `get_assessment_by_id()` method

**Why:** Ensures org_id checking at query level, prevents data leakage

**Risk:** 🟢 LOW - New functions, doesn't replace existing code

---

### TASK 7: Update Assessment Saving to Include org_id

**File:** `src/modules/data/database_manager.py`

**Modify save_assessment() method:**

**Current (lines 42-57):**
```python
# Insert assessment
cursor.execute("""
    INSERT INTO assessments (user_id, assessment_name, framework_version, overall_score, 
                            overall_maturity, completion_percentage, status, submitted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
""", (user_id, ...))
```

**Change to:**
```python
# Get user's org_id
cursor.execute("SELECT org_id FROM users WHERE id=?", (user_id,))
org_result = cursor.fetchone()
org_id = org_result[0] if org_result else None

# Insert assessment with org_id
cursor.execute("""
    INSERT INTO assessments (user_id, org_id, assessment_name, framework_version, overall_score, 
                            overall_maturity, completion_percentage, status, submitted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
""", (user_id, org_id, assessment_name, framework_version, overall.get('percentage', 0), 
      overall.get('maturity_level', 'Unknown'), ...))
```

**Why:** When saving assessment, automatically capture org_id from user

**Risk:** 🟠 MEDIUM - Modifies existing function, needs testing

---

### TASK 8: Update Session State to Track org_id

**File:** `src/app/main.py`

**In initialize_session() function (around line 60):**

**Current:**
```python
required_states = {
    'user': None,
    'logged_in': False,
    ...
}
```

**Add:**
```python
required_states = {
    'user': None,
    'logged_in': False,
    'org_id': None,  # ADD THIS
    'current_page': 'login',
    ...
}
```

**Also update login_user() in shared_navigation.py:**
```python
def login_user(user_data):
    """Login function that works everywhere"""
    st.session_state.user = user_data
    st.session_state.org_id = user_data.get('org_id')  # ADD THIS
    st.session_state.logged_in = True
    st.session_state.current_page = 'assessment'
    st.session_state.assessment_responses = {}
    st.session_state.assessment_completed = False
    st.rerun()
```

**Why:** Tracks organization in session for use in queries

**Risk:** 🟢 LOW - Additive state variable

---

## 📋 IMPLEMENTATION SEQUENCE (SAFE ORDER)

### Phase A: Database Schema (First - No Risk)
1. ✅ Add org_id to users table migration
2. ✅ Add org_id to assessments table migration
3. ✅ Create organizations table
4. ✅ Test app still starts

### Phase B: Data Initialization (Low Risk)
5. ✅ Add demo user auto-creation
6. ✅ Verify demo user created on startup

### Phase C: Session Tracking (Low Risk)
7. ✅ Add org_id to session state
8. ✅ Update login_user() to track org_id

### Phase D: Query Isolation (Medium Risk - Careful!)
9. ✅ Add new isolated query functions
10. ✅ Create multi-tenant validation function
11. ✅ Test new functions with test data

### Phase E: UI Updates (Low Risk)
12. ✅ Restore demo login button
13. ✅ Update assessment saving

### Phase F: Testing & Validation (Critical!)
14. ✅ Clear caches
15. ✅ Restart app multiple times
16. ✅ Test each scenario
17. ✅ Verify no breaking changes

---

## ⏱️ REVISED TIMEFRAME WITH DETAILS

### Priority 1.1: Multi-Tenant Isolation
- Phase A (Database): 30 min
- Phase D (Query functions): 45 min
- Phase F (Testing): 1 hour
- **Subtotal: 2 hours 15 min**

### Priority 1.2: Demo User Restoration
- Phase B (Auto-creation): 30 min
- Phase E (UI button): 15 min
- Phase F (Testing): 30 min
- **Subtotal: 1 hour 15 min**

### Priority 1.3: Organizations Integration
- Phase A (Table creation): 15 min
- Phase B (Demo org): 10 min
- Phase C (Session tracking): 15 min
- Phase F (Testing): 45 min
- **Subtotal: 1 hour 25 min**

**TOTAL: 4 hours 50 min** (vs 5-8 estimated)

---

## ✅ SAFE APPROACH GUARANTEES

### What We're Doing Right
- ✅ **Additive Changes:** Adding new functions, not replacing
- ✅ **Backwards Compatible:** Old code still works
- ✅ **Idempotent Operations:** Safe to restart/re-run
- ✅ **Schema Migrations:** Use ALTER TABLE, not DELETE
- ✅ **Foreign Keys:** Validate data relationships
- ✅ **Rollback Capability:** Easy to undo if needed

### What We're NOT Doing
- ❌ NOT deleting any existing functions
- ❌ NOT removing files
- ❌ NOT breaking existing flows
- ❌ NOT making breaking database changes
- ❌ NOT rushing into testing

---

## 🧪 TESTING PLAN

### Test 1: Database Integrity
```python
✅ Users table has org_id column
✅ Assessments table has org_id column
✅ Organizations table created
✅ Foreign keys are valid
✅ Indexes are created
```

### Test 2: Demo User
```python
✅ Demo user auto-created on first run
✅ Demo user can login with "demo@example.com"
✅ Demo user has role = "demo"
✅ Demo user linked to Demo Organization
```

### Test 3: Multi-Tenant Isolation
```python
✅ User A (Org 1) can see only their assessments
✅ User B (Org 2) cannot see User A's assessments
✅ Queries include org_id filtering
✅ Session tracks org_id correctly
```

### Test 4: No Breaking Changes
```python
✅ App starts without errors
✅ Login/registration still works
✅ Assessment still renders
✅ Results still calculate
✅ No cache conflicts
```

---

## 🚨 RISK MITIGATION

### Risk: Database Corruption
**Mitigation:**
- Use migration functions (ALTER TABLE if not exists)
- Always commit after changes
- Take backup before starting

### Risk: Cache Conflicts
**Mitigation:**
- Clear `__pycache__` before testing
- Restart Streamlit fully (Ctrl+C, then re-run)
- Test multiple times

### Risk: Breaking Existing Flows
**Mitigation:**
- Keep old functions alongside new ones
- Use feature flags to toggle
- Test each change individually

### Risk: Data Integrity
**Mitigation:**
- Validate org_id before querying
- Check foreign keys
- Test with edge cases

---

## 📝 NEXT STEP

Would you like me to:

1. **Create a detailed implementation checklist** with copy-paste ready code?
2. **Show you each change in context** before making it?
3. **Start with Phase A** (database migrations) - safest first step?
4. **Create test scripts** to verify each step works?

What would help you most?

