"""Authentication components for AI Governance Pro"""
import streamlit as st
from modules.auth.auth_manager import auth_manager
from modules.utils.shared_navigation import navigate_to, login_user
from modules.utils.password_validator import PasswordValidator
from modules.utils.audit_logger import AuditLogger
from modules.utils.rate_limiter import RateLimiter

def render_login_page():
    """Professional login page with enterprise design"""
    # CSS Styles for professional appearance
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
        }
        .tagline {
            text-align: center;
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }
        .value-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #f5f3ff 100%);
            border: 1px solid #e0e7ff;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .demo-buttons {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="main-header">🏢 AI Governance Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Enterprise AI Risk Management Assessment</div>', unsafe_allow_html=True)

    # Two column layout
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Value proposition cards
        st.markdown("""
            <div class="value-card">
                <h3>🛡️ Ensure AI Compliance</h3>
                <p>Assess against NIST RMF, ISO 42001, EU AI Act frameworks. Identify gaps before they become liabilities.</p>
            </div>
            <div class="value-card">
                <h3>⚡ Complete in Minutes</h3>
                <p>25 expertly crafted questions across 5 critical domains. Get instant maturity scoring.</p>
            </div>
            <div class="value-card">
                <h3>📊 Executive Reports</h3>
                <p>Generate professional analytics dashboards and export results for stakeholders.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Frameworks", "5x", "Global coverage")
        with col_m2:
            st.metric("Time", "85%", "Faster")
        with col_m3:
            st.metric("Cost", "$0", "To start")

    with col_right:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("🔐 Welcome Back")
        
        st.markdown("---")
        
        # Manual login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="user@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_submitted:
                if email and password:
                    # Check rate limiting
                    is_allowed, message = RateLimiter.check_rate_limit(email)
                    if not is_allowed:
                        st.error(f"❌ {message}")
                        AuditLogger.log_security_event(
                            "rate_limit_exceeded",
                            "warning",
                            {'email': email, 'reason': 'too_many_attempts'}
                        )
                    else:
                        # Distinguish between unknown email and incorrect password
                        if not auth_manager.get_user(email):
                            st.error("❌ Email not registered. Please sign up or reset your password.")
                            AuditLogger.log_authentication(email, False)
                        elif auth_manager.is_account_locked(email):
                            st.error("❌ Account locked due to multiple failed attempts. Please try again later or reset your password.")
                            AuditLogger.log_authentication(email, False)
                        else:
                            user = auth_manager.authenticate(email, password)
                            if user:
                                RateLimiter.reset_attempts(email)
                                AuditLogger.log_authentication(email, True)
                                login_user(user)
                            else:
                                RateLimiter.record_failed_attempt(email)
                                st.error("❌ Incorrect password for this account")
                                AuditLogger.log_authentication(email, False)
                else:
                    st.error("❌ Please enter both email and password")
        
        st.markdown("---")
        # Forgot password
        with st.expander("Forgot password?", expanded=False):
            fp_email = st.text_input("Enter your account email to reset password", value="")
            if st.button("Send reset token", key="send_reset_token"):
                if not fp_email:
                    st.error("❌ Enter your email to receive a reset token")
                else:
                    token, err = auth_manager.create_password_reset_token(fp_email)
                    if err == 'not_found':
                        st.error("❌ Email not found. Please register first.")
                    else:
                        # Since we don't have email delivery in this environment, display the token
                        st.success("✅ Password reset token generated. Use the token to reset your password.")
                        st.code(token)
                        AuditLogger.log_security_event('password_reset_requested', 'info', {'email': fp_email})
        # Reset password using token
        with st.expander("Have a reset token? Reset password", expanded=False):
            rt_token = st.text_input("Reset Token", value="", key="rt_token")
            rt_password = st.text_input("New Password", type="password", key="rt_password")
            rt_confirm = st.text_input("Confirm New Password", type="password", key="rt_confirm")
            if st.button("Reset Password", key="do_reset"):
                if not rt_token or not rt_password or not rt_confirm:
                    st.error("❌ Provide token and new password (and confirm it)")
                elif rt_password != rt_confirm:
                    st.error("❌ Passwords do not match")
                else:
                    ok, reason = auth_manager.reset_password(rt_token, rt_password)
                    if ok:
                        st.success("✅ Password has been reset. Please login with your new password.")
                        AuditLogger.log_security_event('password_reset_completed', 'info', {'token': rt_token})
                    else:
                        st.error(f"❌ Could not reset password: {reason}")
        
        st.markdown("### New to AI Governance Pro?")
        if st.button("🚀 Create Enterprise Account", use_container_width=True, type="secondary"):
            navigate_to("register")
        
        st.caption("No credit card required • Full assessment access")
        st.markdown('</div>', unsafe_allow_html=True)

def render_registration_page():
    """Render the registration page with enhanced security"""
    st.markdown("### 🚀 Join AI Governance Pro")
    st.write("Create your enterprise account to access full assessment capabilities.")
    
    # Display password requirements
    pwd_requirements = PasswordValidator.get_requirements()
    with st.expander("📋 Password Requirements", expanded=False):
        st.write(f"• Minimum {pwd_requirements['min_length']} characters")
        if pwd_requirements['uppercase']:
            st.write("• At least one uppercase letter (A-Z)")
        if pwd_requirements['lowercase']:
            st.write("• At least one lowercase letter (a-z)")
        if pwd_requirements['digits']:
            st.write("• At least one digit (0-9)")
        if pwd_requirements['special_chars']:
            st.write("• At least one special character (!@#$%^&* etc.)")
        st.write(f"• Example: {pwd_requirements['example']}")
    
    with st.form("registration_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Doe")
        
        email = st.text_input("Work Email *", placeholder="user@company.com")
        organization = st.text_input("Organization *", placeholder="Acme Corp")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password *", type="password", 
                                   help="Use strong password with mixed case, numbers, and special characters")
        with col2:
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        industry = st.selectbox("Industry", 
            ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Government", "Education", "Other"])
        
        submitted = st.form_submit_button("🚀 Create Account", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([first_name, last_name, email, organization, password, confirm_password]):
                st.error("❌ All fields marked with * are required")
                return False
            
            if password != confirm_password:
                st.error("❌ Passwords do not match")
                return False
            
            # Validate password strength
            is_valid, message = PasswordValidator.validate(password)
            if not is_valid:
                st.error(f"❌ {message}")
                return False
            
            # Create account
            try:
                success, message = auth_manager.create_user(
                    email=email,
                    password=password,
                    full_name=f"{first_name} {last_name}",
                    organization=organization,
                    role="user"
                )
                
                if success:
                    AuditLogger.log_user_registration(email, organization)
                    st.success("✅ Account created successfully! Please login with your new credentials.")
                    st.balloons()
                    navigate_to("login")
                    return True
                else:
                    st.error(f"❌ {message}")
                    return False
                    
            except Exception as e:
                st.error(f"❌ Registration error: {str(e)}")
                return False
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True):
        navigate_to("login")
    
    return False
from modules.utils.validators import validators

def render_login_page():
    """Professional login page with enterprise design"""
    # CSS Styles for professional appearance
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
        }
        .tagline {
            text-align: center;
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }
        .value-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #f5f3ff 100%);
            border: 1px solid #e0e7ff;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .demo-buttons {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="main-header">🏢 AI Governance Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Enterprise AI Risk Management Assessment</div>', unsafe_allow_html=True)

    # Two column layout
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Value proposition cards
        st.markdown("""
            <div class="value-card">
                <h3>🛡️ Ensure AI Compliance</h3>
                <p>Assess against NIST RMF, ISO 42001, EU AI Act frameworks. Identify gaps before they become liabilities.</p>
            </div>
            <div class="value-card">
                <h3>⚡ Complete in Minutes</h3>
                <p>25 expertly crafted questions across 5 critical domains. Get instant maturity scoring.</p>
            </div>
            <div class="value-card">
                <h3>📊 Executive Reports</h3>
                <p>Generate professional analytics dashboards and export results for stakeholders.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Frameworks", "5x", "Global coverage")
        with col_m2:
            st.metric("Time", "85%", "Faster")
        with col_m3:
            st.metric("Cost", "$0", "To start")

    with col_right:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("🔐 Welcome Back")
        
        # Manual login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="user@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            login_submitted = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_submitted:
                if email and password:
                    # Distinguish email not found vs wrong password
                    if not auth_manager.get_user(email):
                        st.error("❌ Email not registered. Please sign up or reset your password.")
                    elif auth_manager.is_account_locked(email):
                        st.error("❌ Account locked due to failed attempts. Reset your password or try later.")
                    else:
                        user = auth_manager.authenticate(email, password)
                        if user:
                            login_user(user)
                        else:
                            st.error("❌ Incorrect password for this account")
                else:
                    st.error("❌ Please enter both email and password")
        
        st.markdown("---")
        # Forgot password (duplicate section for second login form)
        with st.expander("Forgot password?", expanded=False):
            fp_email = st.text_input("Enter your account email to reset password", value="", key="fp2")
            if st.button("Send reset token", key="send_reset_token_2"):
                if not fp_email:
                    st.error("❌ Enter your email to receive a reset token")
                else:
                    token, err = auth_manager.create_password_reset_token(fp_email)
                    if err == 'not_found':
                        st.error("❌ Email not found. Please register first.")
                    else:
                        st.success("✅ Password reset token generated. Use the token to reset your password.")
                        st.code(token)
                        AuditLogger.log_security_event('password_reset_requested', 'info', {'email': fp_email})
        
        st.markdown("### New to AI Governance Pro?")
        if st.button("�� Create Enterprise Account", use_container_width=True, type="secondary"):
            navigate_to("register")
        
        st.caption("No credit card required • Full assessment access")
        st.markdown('</div>', unsafe_allow_html=True)

def render_registration_page():
    """Render the registration page"""
    st.markdown("### 🚀 Join AI Governance Pro")
    st.write("Create your enterprise account to access full assessment capabilities.")
    
    with st.form("registration_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Doe")
        
        email = st.text_input("Work Email *", placeholder="user@company.com")
        organization = st.text_input("Organization *", placeholder="Acme Corp")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password *", type="password", 
                                   help="Min 8 characters with uppercase, lowercase, digit, and special character")
        with col2:
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        industry = st.selectbox("Industry", 
            ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Government", "Education", "Other"])
        
        submitted = st.form_submit_button("🚀 Create Account", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([first_name, last_name, email, organization, password, confirm_password]):
                st.error("❌ All fields marked with * are required")
                return False
            
            if password != confirm_password:
                st.error("❌ Passwords do not match")
                return False
            
            # Password strength validation
            is_valid, error_msg = validators.validate_password(password)
            if not is_valid:
                st.error(f"❌ {error_msg}")
                return False
            
            # Create account
            try:
                success, message = auth_manager.create_user(
                    email=email,
                    password=password,
                    full_name=f"{first_name} {last_name}",
                    organization=organization,
                    role="user"
                )
                
                if success:
                    st.success("✅ Account created successfully! Please login with your new credentials.")
                    st.balloons()
                    navigate_to("login")
                    return True
                else:
                    st.error(f"❌ {message}")
                    return False
                    
            except Exception as e:
                st.error(f"❌ Registration error: {str(e)}")
                return False
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True):
        navigate_to("login")
    
    return False
