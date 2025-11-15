import streamlit as st
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import json

class EvidenceManager:
    def __init__(self):
        self.evidence_dir = "evidence_uploads"
        self._ensure_evidence_dir()
    
    def _ensure_evidence_dir(self):
        """Create evidence directory if it doesn't exist"""
        if not os.path.exists(self.evidence_dir):
            os.makedirs(self.evidence_dir)
    
    def upload_evidence(self, question_id: str, uploaded_file, description: str = "") -> Dict:
        """Upload and store evidence for a specific question with security validation"""
        try:
            if uploaded_file is not None:
                # Server-side file validation
                file_size = uploaded_file.size
                max_file_size = 10 * 1024 * 1024  # 10MB
                
                # Check file size
                if file_size > max_file_size:
                    st.error(f"File exceeds 10MB limit ({file_size / 1024 / 1024:.1f}MB)")
                    return None
                
                # Validate file type (server-side, not just client-side)
                allowed_mimetypes = [
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'text/plain',
                    'image/png',
                    'image/jpeg',
                    'image/jpg'
                ]
                
                if uploaded_file.type not in allowed_mimetypes:
                    st.error(f"File type '{uploaded_file.type}' not allowed. Allowed: PDF, DOC, DOCX, TXT, PNG, JPG")
                    return None
                
                # Check for path traversal attempts
                filename = uploaded_file.name
                if '..' in filename or '/' in filename or '\\' in filename:
                    st.error("Invalid filename detected")
                    return None
                
                # Generate unique file name (sanitized)
                import re
                safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
                file_extension = safe_filename.split('.')[-1] if '.' in safe_filename else 'bin'
                unique_id = str(uuid.uuid4())[:8]
                file_name = f"{question_id}_{unique_id}.{file_extension}"
                file_path = os.path.join(self.evidence_dir, file_name)
                
                # Save file
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Create evidence record
                evidence_record = {
                    'id': unique_id,
                    'question_id': question_id,
                    'file_name': uploaded_file.name,
                    'stored_name': file_name,
                    'file_size': uploaded_file.size,
                    'file_type': uploaded_file.type,
                    'description': description,
                    'upload_date': datetime.now().isoformat(),
                    'file_path': file_path
                }
                
                # Update session state
                if 'evidence' not in st.session_state:
                    st.session_state.evidence = {}
                
                if question_id not in st.session_state.evidence:
                    st.session_state.evidence[question_id] = []
                
                st.session_state.evidence[question_id].append(evidence_record)
                
                return evidence_record
            return None
            
        except Exception as e:
            st.error(f"Evidence upload failed: {str(e)}")
            return None
    
    def get_question_evidence(self, question_id: str) -> List[Dict]:
        """Get all evidence for a specific question"""
        if 'evidence' in st.session_state and question_id in st.session_state.evidence:
            return st.session_state.evidence[question_id]
        return []
    
    def get_all_evidence(self) -> Dict:
        """Get all evidence across all questions"""
        return st.session_state.get('evidence', {})
    
    def delete_evidence(self, question_id: str, evidence_id: str) -> bool:
        """Delete specific evidence"""
        try:
            if 'evidence' in st.session_state and question_id in st.session_state.evidence:
                # Remove from session state
                st.session_state.evidence[question_id] = [
                    ev for ev in st.session_state.evidence[question_id] 
                    if ev['id'] != evidence_id
                ]
                
                # Remove file if empty
                if not st.session_state.evidence[question_id]:
                    del st.session_state.evidence[question_id]
                
                return True
            return False
        except Exception as e:
            st.error(f"Evidence deletion failed: {str(e)}")
            return False
    
    def get_evidence_summary(self) -> Dict:
        """Get summary of all evidence"""
        evidence = self.get_all_evidence()
        summary = {
            'total_files': 0,
            'total_size': 0,
            'by_question': {},
            'file_types': {}
        }
        
        for question_id, evidence_list in evidence.items():
            summary['by_question'][question_id] = len(evidence_list)
            summary['total_files'] += len(evidence_list)
            
            for evidence_item in evidence_list:
                summary['total_size'] += evidence_item.get('file_size', 0)
                file_type = evidence_item.get('file_type', 'unknown')
                summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
        
        return summary
    
    def render_evidence_upload(self, question_id: str, question_text: str) -> None:
        """Render evidence upload interface for a question"""
        with st.expander("📎 Attach Supporting Evidence", expanded=False):
            st.caption(f"Upload documents supporting your response to: *{question_text}*")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                uploaded_file = st.file_uploader(
                    "Choose evidence file",
                    type=['pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
                    key=f"file_upload_{question_id}"
                )
            
            with col2:
                description = st.text_input(
                    "Description",
                    placeholder="Brief description...",
                    key=f"desc_{question_id}"
                )
            
            if uploaded_file and st.button("Upload Evidence", key=f"upload_btn_{question_id}"):
                evidence_record = self.upload_evidence(question_id, uploaded_file, description)
                if evidence_record:
                    st.success(f"✅ Evidence uploaded: {uploaded_file.name}")
                    st.rerun()
            
            # Show existing evidence
            existing_evidence = self.get_question_evidence(question_id)
            if existing_evidence:
                st.markdown("**Uploaded Evidence:**")
                for evidence in existing_evidence:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"📄 {evidence['file_name']}")
                        if evidence['description']:
                            st.caption(f"*{evidence['description']}*")
                    with col2:
                        st.write(f"{evidence['file_size'] // 1024} KB")
                    with col3:
                        if st.button("🗑️", key=f"del_{evidence['id']}"):
                            self.delete_evidence(question_id, evidence['id'])
                            st.rerun()

# Global instance
evidence_manager = EvidenceManager()