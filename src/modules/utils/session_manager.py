"""
ROBUST SESSION MANAGEMENT SYSTEM
Centralized state management for AI Governance Pro
"""
import streamlit as st
from datetime import datetime, timedelta
import hashlib

class SessionManager:
    def __init__(self):
        self.session_timeout = timedelta(hours=2)
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize all session state variables with defaults"""
        defaults = {
            # Authentication
            'user': None,
            'logged_in': False,
            'user_role': 'guest',
            
            # Navigation
            'current_page': 'login',
            'previous_page': None,
            
            # Assessment
            'assessment_started': False,
            'assessment_completed': False,
            'assessment_responses': {},
            'assessment_scores': None,
            'current_domain': None,
            'current_question_index': 0,
            
            # UI State
            'dark_mode': False,
            'sidebar_collapsed': False,
            
            # Security
            'session_id': self._generate_session_id(),
            'last_activity': datetime.now(),
            
            # Demo Limitations
            'demo_questions_answered': 0,
            'max_demo_questions': 10
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def _generate_session_id(self):
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())
    
    def validate_session(self):
        """Validate session is still active and secure"""
        if not st.session_state.logged_in:
            return False
        
        # Check session timeout
        time_since_activity = datetime.now() - st.session_state.last_activity
        if time_since_activity > self.session_timeout:
            self.logout()
            return False
        
        # Update last activity
        st.session_state.last_activity = datetime.now()
        return True
    
    def login_user(self, user_data):
        """Secure user login with session initialization"""
        st.session_state.user = user_data
        st.session_state.logged_in = True
        st.session_state.user_role = user_data.get('role', 'user')
        st.session_state.last_activity = datetime.now()
        
        # Initialize assessment state
        st.session_state.assessment_responses = {}
        st.session_state.assessment_completed = False
        st.session_state.current_page = 'assessment'
        
        # Apply demo limitations
        if st.session_state.user_role == 'demo':
            st.session_state.demo_questions_answered = 0
            st.session_state.max_demo_questions = 10
    
    def logout(self):
        """Secure logout with complete state cleanup"""
        keys_to_preserve = ['dark_mode']  # Preserve UI preferences
        
        preserved = {}
        for key in keys_to_preserve:
            if key in st.session_state:
                preserved[key] = st.session_state[key]
        
        # Clear all session state
        st.session_state.clear()
        
        # Restore preserved values
        for key, value in preserved.items():
            st.session_state[key] = value
        
        # Re-initialize defaults
        self._initialize_session_state()
    
    def navigate_to(self, page):
        """Safe navigation with state validation"""
        if self.validate_session() or page in ['login', 'register']:
            st.session_state.previous_page = st.session_state.current_page
            st.session_state.current_page = page
            st.session_state.last_activity = datetime.now()
            return True
        return False
    
    def save_response(self, question_id, response):
        """Save assessment response with validation"""
        if not self.validate_session():
            return False
        
        st.session_state.assessment_responses[question_id] = {
            'response': response,
            'timestamp': datetime.now(),
            'question_id': question_id
        }
        
        # Track demo question usage
        if st.session_state.user_role == 'demo':
            st.session_state.demo_questions_answered = len(st.session_state.assessment_responses)
        
        return True
    
    def can_answer_more_questions(self):
        """Check if user can answer more questions (demo limitations)"""
        if st.session_state.user_role != 'demo':
            return True
        
        return st.session_state.demo_questions_answered < st.session_state.max_demo_questions

# Global session manager instance
session_manager = SessionManager()
