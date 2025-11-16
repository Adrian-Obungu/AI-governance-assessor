import streamlit as st
import sys
import os

# Add path for modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Force dark mode compatibility
st.markdown("""
<style>
* {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# Simple session management
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.set_page_config(
        page_title="AI Governance Pro", 
        page_icon="🏢",
        layout="wide"
    )
    
    if st.session_state.page == 'login':
        render_login()
    elif st.session_state.page == 'assessment':
        render_assessment()
    elif st.session_state.page == 'results':
        render_results()

def render_login():
    st.title("🏢 AI Governance Pro")
    st.write("Enterprise AI Risk Management Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Transform Your AI Governance")
        st.write("• Assess against NIST RMF, ISO 42001, EU AI Act")
        st.write("• 25 questions across 5 critical domains") 
        st.write("• Professional analytics and reporting")
    
    with col2:
        st.subheader("Login")
        
        if st.button("👤 Demo User Login", key="demo_login"):
            st.session_state.user = {"name": "Demo User", "role": "demo"}
            st.session_state.page = 'assessment'
            st.success("Login successful!")
            st.rerun()
            
        if st.button("�� Admin Demo Login", key="admin_login"):
            st.session_state.user = {"name": "Admin User", "role": "admin"} 
            st.session_state.page = 'assessment'
            st.success("Login successful!")
            st.rerun()
        
        st.markdown("---")
        
        if st.button("📝 Create Account", key="create_account"):
            st.session_state.page = 'register'
            st.rerun()

def render_assessment():
    if not st.session_state.user:
        st.session_state.page = 'login'
        st.rerun()
    
    st.title("📊 AI Governance Assessment")
    st.write(f"Welcome, {st.session_state.user['name']}")
    
    if st.session_state.user['role'] == 'demo':
        st.info("🔒 Demo Mode: Limited functionality")
    
    # Simple assessment
    st.subheader("Governance & Strategy")
    q1 = st.radio(
        "How mature is your AI governance framework?",
        ["Not Started", "Initial", "Developing", "Established", "Advanced"],
        key="q1"
    )
    
    st.subheader("Risk Management")
    q2 = st.radio(
        "How do you identify and manage AI risks?",
        ["Not Started", "Initial", "Developing", "Established", "Advanced"], 
        key="q2"
    )
    
    if st.button("✅ Submit Assessment", type="primary", key="submit"):
        st.session_state.page = 'results'
        st.rerun()
    
    st.markdown("---")
    if st.button("🚪 Logout", key="logout_assess"):
        st.session_state.user = None
        st.session_state.page = 'login'
        st.rerun()

def render_results():
    if not st.session_state.user:
        st.session_state.page = 'login'
        st.rerun()
    
    st.title("📈 Assessment Results")
    
    st.metric("Overall Score", "68%")
    st.metric("Maturity Level", "Developing")
    
    st.subheader("Domain Performance")
    st.write("• Governance & Strategy: 75%")
    st.write("• Risk Management: 60%")
    st.write("• Lifecycle Management: 65%")
    st.write("• Transparency: 70%") 
    st.write("• Compliance: 70%")
    
    st.info("Detailed analytics and recommendations available in full version")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 New Assessment", key="new_assess"):
            st.session_state.page = 'assessment'
            st.rerun()
    with col2:
        if st.button("🚪 Logout", key="logout_results"):
            st.session_state.user = None
            st.session_state.page = 'login'
            st.rerun()

if __name__ == "__main__":
    main()
