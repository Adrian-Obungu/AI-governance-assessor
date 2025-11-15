"""
INTEGRATION BRIDGE
Connects auth_components with main.py session management
"""
import streamlit as st
import sys
import os

# Import the session functions from main
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
try:
    from main import navigate_to, login_user
except ImportError:
    # Fallback functions if import fails
    def navigate_to(page):
        st.session_state.current_page = page
        st.rerun()
    
    def login_user(user_data):
        st.session_state.user = user_data
        st.session_state.logged_in = True
        st.session_state.current_page = 'assessment'
        st.rerun()
