"""Main application entry point"""
import sys, os
import streamlit as st
from modules.auth.auth_components import render_login_page
from modules.assessment.engine import render_assessment, show_assessment_results
from modules.utils.navigation_manager import nav_manager
from modules.utils.analytics_dashboard import render_analytics


def main():
    """Main application entry point"""
    # Initialize session state
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "assessment"
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    # App config
    st.set_page_config(
        page_title="AI Governance Pro",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Route based on current page
    if not st.session_state.user:
        render_login_page()
    else:
        # Register pages if not already done
        if len(nav_manager.pages) == 0:
            nav_manager.register_page("assessment", render_assessment)
            nav_manager.register_page("analytics", show_assessment_results)
            nav_manager.register_page("admin", render_analytics)
        
        # Render current page
        nav_manager.render_current_page()


if __name__ == "__main__":
    main()
