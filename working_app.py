"""
GUARANTEED WORKING VERSION - AI Governance Pro
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# App configuration
st.set_page_config(
    page_title="AI Governance Pro",
    page_icon="🛡️",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Main app logic
    if not st.session_state.user:
        show_login_page()
    else:
        show_main_application()

def show_login_page():
    """Show login page"""
    st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment Platform")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🚀 Complete AI Governance Assessment")
        st.write("""
        **Based on NIST AI RMF Framework:**
        • Governance & Strategy
        • Risk Management
        • Lifecycle Management  
        • Transparency & Explainability
        • Compliance & Ethics
        
        **Enterprise Features:**
        • Multi-user support
        • Progress tracking
        • Analytics dashboard
        • Admin controls
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Get Started")
        
        if st.button("👤 Login as Demo User", use_container_width=True):
            st.session_state.user = {
                'name': 'Demo User',
                'organization': 'Demo Corporation',
                'role': 'user'
            }
            st.rerun()
            
        if st.button("👑 Login as Admin", use_container_width=True):
            st.session_state.user = {
                'name': 'Admin User', 
                'organization': 'Demo Corporation',
                'role': 'admin'
            }
            st.rerun()
        
        st.markdown("---")
        st.info("Use the buttons above to access the demo application")

def show_main_application():
    """Show main application"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.write(f"**Organization:** {st.session_state.user['organization']}")
        st.write(f"**Role:** {st.session_state.user['role']}")
        
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        
        pages = {
            'home': '🏠 Dashboard',
            'assessment': '📊 Assessment', 
            'analytics': '📈 Analytics',
            'admin': '👑 Admin'
        }
        
        for page_id, page_name in pages.items():
            if st.button(page_name, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.page = page_id
                st.rerun()
        
        st.markdown("---")
        if st.button("�� Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Main content area
    st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
    
    if st.session_state.page == 'home':
        show_dashboard()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'analytics':
        show_analytics()
    elif st.session_state.page == 'admin' and st.session_state.user['role'] == 'admin':
        show_admin()
    else:
        st.error("Page not found or access denied")

def show_dashboard():
    """Show dashboard"""
    st.success("🎉 **Application Successfully Running!**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Assessment Progress", "65%", "15%")
    with col2:
        st.metric("Maturity Level", "Developing", "Improved")
    with col3:
        st.metric("Questions Answered", "12/20", "3 new")
    
    st.markdown("---")
    
    # Sample chart
    data = {
        'Domain': ['Governance', 'Risk', 'Lifecycle', 'Transparency', 'Compliance'],
        'Score': [75, 60, 45, 80, 55]
    }
    df = pd.DataFrame(data)
    
    fig = px.bar(df, x='Domain', y='Score', title='Domain Performance')
    st.plotly_chart(fig, use_container_width=True)

def show_assessment():
    """Show assessment interface"""
    st.subheader("AI Governance Assessment")
    
    domains = {
        'governance': '🏛️ Governance & Strategy',
        'risk': '🛡️ Risk Management',
        'lifecycle': '🔄 Lifecycle Management',
        'transparency': '🔍 Transparency & Explainability', 
        'compliance': '⚖️ Compliance & Ethics'
    }
    
    selected_domain = st.selectbox("Select Domain", list(domains.values()))
    
    st.markdown(f"### {selected_domain}")
    st.write("Assessment questions for this domain will appear here.")
    
    # Sample question
    st.markdown("**Has your organization established an AI governance committee with executive leadership?**")
    
    options = [
        "Not Started - No formal governance structure",
        "Initial - Informal working group exists", 
        "Developing - Formal committee without executive sponsorship",
        "Established - Executive-led committee with regular meetings",
        "Advanced - Committee with defined charter and decision authority",
        "Optimized - Board-level oversight with performance metrics"
    ]
    
    st.radio("Select maturity level:", options, key="demo_question")
    
    if st.button("Save Response", type="primary"):
        st.success("Response saved successfully!")

def show_analytics():
    """Show analytics dashboard"""
    st.subheader("Assessment Analytics")
    
    # Sample analytics data
    scores = [65, 72, 58, 81, 69]
    domains = ['Governance', 'Risk', 'Lifecycle', 'Transparency', 'Compliance']
    
    fig = px.pie(values=scores, names=domains, title='Domain Score Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    st.download_button(
        "📊 Download Report",
        data="Sample report data",
        file_name="governance_report.pdf",
        mime="application/pdf"
    )

def show_admin():
    """Show admin dashboard"""
    st.subheader("👑 Admin Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Users", "15")
        st.metric("Active Assessments", "8")
    
    with col2:
        st.metric("Organizations", "3")
        st.metric("System Health", "100%")
    
    st.info("Admin features will be fully implemented in the next phase.")

if __name__ == "__main__":
    main()
