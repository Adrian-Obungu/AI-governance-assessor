"""
CLEAN START - AI Governance Pro
Let's build forward from a working foundation
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# App configuration
st.set_page_config(
    page_title="AI Governance Pro",
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
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
    .domain-pill {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
    }
    .domain-pill:hover {
        background: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session():
    """Initialize clean session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_domain' not in st.session_state:
        st.session_state.current_domain = 'governance'
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

def get_framework():
    """Return the assessment framework"""
    return {
        "governance": {
            "name": "🏛️ Governance & Strategy",
            "questions": [
                {
                    "id": "GOV1",
                    "text": "Has your organization established an AI governance committee with executive leadership?",
                    "maturity_levels": [
                        {"score": 0, "text": "Not Started - No formal governance structure"},
                        {"score": 1, "text": "Initial - Informal working group exists"},
                        {"score": 2, "text": "Developing - Formal committee without executive sponsorship"},
                        {"score": 3, "text": "Established - Executive-led committee with regular meetings"},
                        {"score": 4, "text": "Advanced - Committee with defined charter and decision authority"},
                        {"score": 5, "text": "Optimized - Board-level oversight with performance metrics"}
                    ]
                }
            ]
        }
    }

def render_sidebar():
    """Render clean sidebar"""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        framework = get_framework()
        for domain_id, domain_data in framework.items():
            if st.button(
                f"**{domain_data['name']}**",
                key=f"nav_{domain_id}",
                use_container_width=True,
                type="primary" if st.session_state.current_domain == domain_id else "secondary"
            ):
                st.session_state.current_domain = domain_id
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 👤 User")
        if st.session_state.authenticated:
            st.write(f"**Name:** {st.session_state.user.get('name', 'User')}")
            st.write(f"**Organization:** {st.session_state.user.get('organization', 'Unknown')}")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
        else:
            if st.button("🔐 Login as Demo User"):
                st.session_state.authenticated = True
                st.session_state.user = {
                    'id': 1,
                    'name': 'Demo User',
                    'organization': 'Demo Corp',
                    'role': 'user'
                }
                st.rerun()

def render_assessment():
    """Render clean assessment interface"""
    st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
    st.caption("Enterprise AI Risk Management Assessment")
    
    render_sidebar()
    
    framework = get_framework()
    domain = framework[st.session_state.current_domain]
    
    st.markdown(f"### {domain['name']}")
    
    for question in domain['questions']:
        st.markdown(f"**{question['text']}**")
        
        options = [opt['text'] for opt in question['maturity_levels']]
        current_answer = st.session_state.responses.get(question['id'])
        
        selected = st.radio(
            "Select maturity level:",
            options=options,
            index=current_answer if current_answer is not None else 0,
            key=f"q_{question['id']}",
            label_visibility="collapsed"
        )
        
        # Save response
        for idx, opt in enumerate(question['maturity_levels']):
            if opt['text'] == selected:
                st.session_state.responses[question['id']] = opt['score']
                break

def main():
    """Main application"""
    initialize_session()
    
    if not st.session_state.authenticated:
        st.markdown('<div class="main-header">AI Governance Pro</div>', unsafe_allow_html=True)
        st.caption("Enterprise AI Risk Management Assessment Platform")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("""
            **Welcome to AI Governance Pro**
            
            This tool helps organizations assess their AI governance maturity 
            based on the NIST AI RMF framework.
            
            **Features:**
            • Multi-domain assessment
            • Progress tracking
            • Analytics and reporting
            • Enterprise-ready architecture
            """)
        
        with col2:
            st.subheader("Get Started")
            if st.button("🔐 Login as Demo User", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user = {
                    'id': 1,
                    'name': 'Demo User', 
                    'organization': 'Demo Corporation',
                    'role': 'user'
                }
                st.rerun()
            
            if st.button("👑 Login as Admin", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user = {
                    'id': 1,
                    'name': 'Admin User',
                    'organization': 'Demo Corporation', 
                    'role': 'admin'
                }
                st.rerun()
    else:
        render_assessment()

if __name__ == "__main__":
    main()
