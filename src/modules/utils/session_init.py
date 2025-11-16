"""
SESSION INITIALIZATION
Ensures all required session state variables exist
"""
import streamlit as st

def initialize_session():
    """Initialize all required session state variables"""
    required_states = {
        'user': None,
        'logged_in': False,
        'current_page': 'login',
        'assessment_responses': {},
        'assessment_completed': False,
        'assessment_scores': None
    }
    
    for key, default_value in required_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def ensure_logged_in():
    """Ensure user is logged in, redirect if not"""
    if not st.session_state.logged_in or not st.session_state.user:
        st.session_state.current_page = 'login'
        st.rerun()
        return False
    return True
