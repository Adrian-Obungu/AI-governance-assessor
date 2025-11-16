"""
AI GOVERNANCE PRO - ENTERPRISE EDITION
Professional UI with working functionality
"""
import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import working components
from modules.auth.auth_components import render_login_page, render_registration_page
from modules.assessment.engine import render_assessment, show_assessment_results

# ENTERPRISE DARK MODE FIX
ENTERPRISE_CSS = """
    <style>
    /* Comprehensive dark mode fix */
    .stApp, .main, .block-container {
        color: #000000 !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label, strong, em {
        color: #000000 !important;
    }
    .stButton button, .stDownloadButton button {
        color: #000000 !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        color: #000000 !important;
    }
    .stRadio label, .stCheckbox label {
        color: #000000 !important;
    }
    
    /* Professional header styling */
    .enterprise-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Value proposition cards */
    .value-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #f5f3ff 100%);
        border: 1px solid #e0e7ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    </style>
"""

# Initialize session state
def initialize_session():
    required_states = {
        'user': None,
        'logged_in': False,
        'current_page': 'login',
        'assessment_responses': {},
        'assessment_completed': False,
        'assessment_scores': None
    }
    for key, default in required_states.items():
        if key not in st.session_state:
            st.session_state[key] = default

from modules.utils.shared_navigation import navigate_to, login_user, logout_user

def render_assessment_page():
    """Professional assessment page"""
    if not st.session_state.logged_in:
        navigate_to('login')
        return
    
    # Apply enterprise styling
    st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)
    
    # Professional header
    st.markdown('<div class="enterprise-header">🏢 AI Governance Pro</div>', unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment Platform")
    
    # User welcome
    user = st.session_state.user
    if user:
        st.write(f"**Welcome, {user.get('full_name', 'User')}**")
    else:
        st.write("**Welcome, User**")
        navigate_to('login')
    
    # Demo limitations
    if user.get('role') == 'demo':
        st.info("🔒 Demo Mode: Limited to 10 questions")
    
    # Render assessment
    try:
        render_assessment()
    except Exception as e:
        st.error(f"Error loading assessment: {str(e)}")
        if st.button("Return to Login"):
            logout_user()
    
    # Professional navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            logout_user()
    with col2:
        if st.button("📊 View Results", use_container_width=True, type="secondary", key="results_btn"):
            if st.session_state.assessment_responses:
                navigate_to('results')
            else:
                st.warning("Complete questions to view results")

def render_results_page():
    """Professional results page"""
    if not st.session_state.logged_in:
        navigate_to('login')
        return
    
    # Apply enterprise styling
    st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)
    
    st.markdown('<div class="enterprise-header">📊 Assessment Results</div>', unsafe_allow_html=True)
    
    try:
        show_assessment_results()
    except Exception as e:
        st.error(f"Error loading results: {str(e)}")
        st.info("Complete the assessment to see results")
    
    # Professional navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 New Assessment", use_container_width=True, key="new_assess_btn"):
            st.session_state.assessment_responses = {}
            st.session_state.assessment_completed = False
            navigate_to('assessment')
    with col2:
        if st.button("�� Logout", use_container_width=True, type="secondary", key="logout_results_btn"):
            logout_user()

def main():
    """Main application"""
    # Initialize session
    initialize_session()
    
    # Set page config
    st.set_page_config(
        page_title="AI Governance Pro - Enterprise Edition",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply global styling
    st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)
    
    # Route pages
    current_page = st.session_state.current_page
    
    if current_page == 'login':
        render_login_page()
    elif current_page == 'register':
        render_registration_page()
    elif current_page == 'assessment':
        render_assessment_page()
    elif current_page == 'results':
        render_results_page()
    else:
        navigate_to('login')

if __name__ == "__main__":
    main()
