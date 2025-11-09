"""Authentication UI components"""
import streamlit as st
from .auth_manager import auth_manager

def render_login_page():
    """Render login page"""
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
    
    st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
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
            st.session_state.user = auth_manager.authenticate('user@demo.com', 'demo')
            st.rerun()
        
        if st.button("👑 Admin User Login", use_container_width=True):
            st.session_state.user = auth_manager.authenticate('admin@demo.com', 'demo')  
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
