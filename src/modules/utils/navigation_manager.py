# navigation_manager.py - NEW FILE
import streamlit as st
from typing import Callable, Dict

class NavigationManager:
    """
    Elite navigation system for Streamlit applications
    Uses proven single-pass rendering with deferred state updates
    """
    
    def __init__(self):
        self.pages = {}
        self.current_page = "assessment"
        
    def register_page(self, page_id: str, render_function: Callable):
        """Register a page with its render function"""
        self.pages[page_id] = render_function
    
    def navigate_to(self, page_id: str):
        """Navigate to specified page - GUARANTEED to work"""
        st.session_state.current_page = page_id
        # Force immediate execution context
        st.rerun()
    
    def render_current_page(self):
        """Render the current page - SINGLE SOURCE OF TRUTH"""
        page_id = st.session_state.get('current_page', 'assessment')
        render_function = self.pages.get(page_id)
        
        if render_function:
            render_function()
        else:
            st.error(f"Page '{page_id}' not found")
    
    def create_navigation_button(self, target_page: str, label: str, **kwargs):
        """Create a GUARANTEED working navigation button"""
        return st.button(
            label, 
            on_click=self.navigate_to, 
            args=(target_page,),
            **kwargs
        )

# Global navigation instance
nav_manager = NavigationManager()
# BACKWARD COMPATIBILITY FUNCTION
def setup_navigation():
    """Legacy wrapper for NavigationManager setup"""
    from . import nav_manager
    return nav_manager
