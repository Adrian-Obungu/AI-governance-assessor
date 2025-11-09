"""Authentication UI components"""
import streamlit as st
from .auth_manager import auth_manager


def show_registration_form():
    """Render user registration form"""
    st.markdown("### 📝 Create New Account")

    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Doe")

        email = st.text_input("Email Address", placeholder="user@company.com")
        organization = st.text_input("Organization", placeholder="Acme Corp")

        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", help="Min 8 characters")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password")

        industry = st.selectbox("Industry",
            ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Government", "Education", "Other"])

        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submitted:
            # Validation
            if not all([first_name, last_name, email, organization, password]):
                st.error("All fields are required")
                return False

            if password != confirm_password:
                st.error("Passwords do not match")
                return False

            if len(password) < 8:
                st.error("Password must be at least 8 characters")
                return False

            # Create account
            try:
                user = auth_manager.create_user(
                    email=email,
                    password=password,
                    full_name=f"{first_name} {last_name}",
                    organization=organization,
                    industry=industry,
                    role="user"
                )

                if user:
                    st.success("✅ Account created successfully! Please login.")
                    return True
                else:
                    st.error("Account creation failed. Email may already exist.")
                    return False
                    
            except Exception as e:
                st.error(f"Registration error: {str(e)}")
                return False

    return False


def render_login_page():
    """Enhanced login page with registration option"""
    # Check if user wants to register
    if st.session_state.get("show_registration", False):
        # Show registration form
        success = show_registration_form()
        if success:
            st.session_state.show_registration = False
            st.rerun()
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.show_registration = False
            st.rerun()
        return

    # Main login UI
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="main-header">AI Governance Pro</div>""", unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment Platform")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("""
        **Complete AI Governance Assessment**
        
        Based on NIST AI RMF Framework:
        • Governance & Strategy
        • Risk Management  
        • Lifecycle Management
        • Transparency & Explainability
        • Compliance & Ethics
        """)
    
    with col2:
        st.subheader("Login")
        
        # Demo login buttons
        if st.button("👤 Demo User Login", use_container_width=True):
            st.session_state.user = auth_manager.authenticate("user@demo.com", "demo")
            st.rerun()
        
        if st.button("👑 Admin User Login", use_container_width=True):
            st.session_state.user = auth_manager.authenticate("admin@demo.com", "demo")  
            st.rerun()
        
        # Manual login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="user@company.com")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                user = auth_manager.authenticate(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    st.markdown("---")
    st.markdown("### New User?")
    if st.button("📝 Create New Account", use_container_width=True, type="secondary"):
        st.session_state.show_registration = True
        st.rerun()
