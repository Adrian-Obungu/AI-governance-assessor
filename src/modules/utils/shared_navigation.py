"""
SHARED NAVIGATION UTILITIES
Functions that can be imported by both main.py and auth_components.py
"""
import streamlit as st

def navigate_to(page):
    """Simple navigation that works everywhere"""
    st.session_state.current_page = page
    st.rerun()

def login_user(user_data):
    """Login function that works everywhere"""
    st.session_state.user = user_data
    st.session_state.logged_in = True
    st.session_state.current_page = 'assessment'
    st.session_state.assessment_responses = {}
    st.session_state.assessment_completed = False
    st.rerun()

def logout_user():
    """Logout function that works everywhere"""
    st.session_state.user = None
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.assessment_responses = {}
    st.session_state.assessment_completed = False
    st.session_state.assessment_scores = None
    st.rerun()
