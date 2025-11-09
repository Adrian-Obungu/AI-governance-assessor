"""
AI Governance Pro - Main Application
Clean, working version with proper structure
"""
import streamlit as st
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import from our new modules
from modules.auth.auth_manager import auth_manager
from modules.auth.auth_components import render_login_page
from modules.assessment.framework import get_assessment_framework
from modules.assessment.engine import AssessmentEngine

def main():
    """Main application entry point"""
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_domain' not in st.session_state:
        st.session_state.current_domain = 'governance'
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # App config
    st.set_page_config(
        page_title="AI Governance Pro",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check authentication
    if not st.session_state.user:
        render_login_page()
    else:
        render_main_application()

def render_main_application():
    """Render the main assessment interface"""
    st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment")
    
    # Render sidebar navigation
    render_sidebar()
    
    # Render current domain assessment
    render_domain_assessment()

def render_sidebar():
    """Render application sidebar"""
    with st.sidebar:
        # User info
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.write(f"**Organization:** {st.session_state.user['organization']}")
        st.write(f"**Role:** {st.session_state.user['role']}")
        
        st.markdown("---")
        st.markdown("### 🧭 Assessment Domains")
        
        framework = get_assessment_framework()
        for domain_id, domain_data in framework.items():
            if st.button(
                domain_data['name'],
                key=f"nav_{domain_id}",
                use_container_width=True,
                type="primary" if st.session_state.current_domain == domain_id else "secondary"
            ):
                st.session_state.current_domain = domain_id
                st.rerun()
        
        st.markdown("---")
        if st.button("�� Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

def render_domain_assessment():
    """Render assessment for current domain"""
    framework = get_assessment_framework()
    domain = framework[st.session_state.current_domain]
    
    st.markdown(f"## {domain['name']}")
    st.write(domain['description'])
    
    # Render questions
    engine = AssessmentEngine()
    for question in domain['questions']:
        engine.render_question(question)

if __name__ == "__main__":
    main()
