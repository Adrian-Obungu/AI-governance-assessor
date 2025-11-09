import streamlit as st
import json
import uuid
from datetime import datetime
from typing import Dict, Any

class SessionManager:
    def __init__(self):
        self.sessions_dir = "saved_sessions"
    
    def save_session(self, session_data: Dict, session_name: str = None) -> str:
        """Save current session to file"""
        try:
            if session_name is None:
                session_name = f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            session_id = str(uuid.uuid4())[:8]
            
            # Prepare session data
            save_data = {
                'session_id': session_id,
                'session_name': session_name,
                'save_date': datetime.now().isoformat(),
                'data': session_data
            }
            
            # Store in session state
            if 'saved_sessions' not in st.session_state:
                st.session_state.saved_sessions = {}
            
            st.session_state.saved_sessions[session_id] = save_data
            
            # For download
            return json.dumps(save_data, indent=2)
            
        except Exception as e:
            st.error(f"Session save failed: {str(e)}")
            return None
    
    def load_session(self, session_data: str) -> bool:
        """Load session from JSON data"""
        try:
            session_dict = json.loads(session_data)
            
            # Restore session state
            if 'data' in session_dict:
                data = session_dict['data']
                
                # Restore responses
                if 'responses' in data:
                    st.session_state.responses = data['responses']
                
                # Restore user info
                if 'user_info' in data:
                    st.session_state.user_info = data['user_info']
                
                # Restore evidence
                if 'evidence' in data:
                    st.session_state.evidence = data['evidence']
                
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Session load failed: {str(e)}")
            return False
    
    def get_session_data(self) -> Dict:
        """Get current session data for saving"""
        return {
            'responses': st.session_state.get('responses', {}),
            'user_info': st.session_state.get('user_info', {}),
            'evidence': st.session_state.get('evidence', {}),
            'timestamp': datetime.now().isoformat()
        }
    
    def render_session_management(self):
        """Render session management interface with improved UI"""
        with st.expander("💾 Session Management", expanded=False):
            
            # Save Session Section
            st.subheader("Save Current Session")
            
            session_name = st.text_input(
                "Session Name",
                value=f"assessment_{datetime.now().strftime('%Y%m%d')}",
                help="Name for this assessment session",
                key="session_name_input"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("💾 Save Session", use_container_width=True, key="save_session_btn"):
                    session_data = self.get_session_data()
                    json_data = self.save_session(session_data, session_name)
                    
                    if json_data:
                        st.success("✅ Session saved!")
                        
                        # Show download button
                        st.download_button(
                            "📥 Download Session File",
                            json_data,
                            file_name=f"{session_name}.json",
                            mime="application/json",
                            use_container_width=True,
                            key="download_session_btn"
                        )
            
            with col2:
                if st.button("🔄 Refresh", use_container_width=True, key="refresh_btn"):
                    st.rerun()
            
            st.markdown("---")
            
            # Load Session Section
            st.subheader("Load Session")
            
            uploaded_session = st.file_uploader(
                "Choose session file",
                type=['json'],
                help="Upload a previously saved session file",
                key="session_uploader"
            )
            
            if uploaded_session is not None:
                file_details = {
                    "FileName": uploaded_session.name,
                    "FileType": uploaded_session.type,
                    "FileSize": f"{uploaded_session.size} bytes"
                }
                
                st.write("**File Details:**")
                st.json(file_details, expanded=False)
                
                if st.button("🔄 Load Uploaded Session", use_container_width=True, key="load_session_btn"):
                    try:
                        session_data = uploaded_session.getvalue().decode()
                        if self.load_session(session_data):
                            st.success("✅ Session loaded successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to load session data")
                    except Exception as e:
                        st.error(f"❌ Error loading session: {str(e)}")
            
            # Session Statistics
            if st.session_state.get('responses'):
                st.markdown("---")
                st.subheader("Session Statistics")
                
                col1, col2 = st.columns(2)
                with col1:
                    answered = len([v for v in st.session_state.responses.values() if v is not None])
                    st.metric("Questions Answered", answered)
                
                with col2:
                    if 'evidence' in st.session_state:
                        evidence_count = sum(len(ev_list) for ev_list in st.session_state.evidence.values())
                        st.metric("Evidence Files", evidence_count)

# Global instance
session_manager = SessionManager()
# BACKWARD COMPATIBILITY FUNCTION
def initialize_session():
    """Legacy wrapper for SessionManager initialization"""
    return SessionManager()
