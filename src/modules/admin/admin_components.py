import streamlit as st

def render_admin_dashboard():
    """Render admin dashboard"""
    st.markdown('<div class="main-header">👑 Admin Dashboard</div>', unsafe_allow_html=True)
    st.info("Admin features will be implemented here.")
    st.write("User management, organization analytics, and system settings coming soon.")

def is_admin_user():
    """Check if current user is admin"""
    user = st.session_state.get('user', {})
    return user.get('role') == 'admin'
