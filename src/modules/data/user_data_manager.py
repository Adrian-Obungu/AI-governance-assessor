# modules/user_data_manager.py - NEW FILE FOR USER DATA ISOLATION
import streamlit as st
from modules.data.database_manager import db_manager

class UserDataManager:
    def __init__(self):
        self.db_manager = db_manager
    
    def get_current_user_id(self):
        """Get current user ID from session"""
        if st.session_state.get('user'):
            return st.session_state.user['id']
        return None
    
    def save_user_assessment(self, assessment_name: str = None) -> int:
        """Save current assessment for the logged-in user"""
        user_id = self.get_current_user_id()
        if not user_id:
            st.error("User not authenticated")
            return None
        
        if not assessment_name:
            assessment_name = f"Assessment_{st.session_state.user['organization']}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        try:
            scores = self.calculate_scores()
            assessment_id = self.db_manager.save_assessment(
                st.session_state.user_info,
                scores,
                assessment_name,
                user_id
            )
            return assessment_id
        except Exception as e:
            st.error(f"Failed to save assessment: {e}")
            return None
    
    def get_user_assessments(self):
        """Get all assessments for the current user"""
        user_id = self.get_current_user_id()
        if not user_id:
            return []
        
        return self.db_manager.get_assessment_history(user_id=user_id)
    
    def load_user_assessment(self, assessment_id: int) -> dict:
        """Load a specific assessment for the current user"""
        user_id = self.get_current_user_id()
        if not user_id:
            return None
        
        return self.db_manager.load_assessment(assessment_id, user_id)
    
    def get_user_statistics(self) -> dict:
        """Get statistics for the current user"""
        user_id = self.get_current_user_id()
        if not user_id:
            return {}
        
        return self.db_manager.get_user_stats(user_id)
    
    def export_user_data(self) -> pd.DataFrame:
        """Export all data for the current user"""
        user_id = self.get_current_user_id()
        if not user_id:
            return pd.DataFrame()
        
        return self.db_manager.export_user_data(user_id)
    
    def calculate_scores(self):
        """Calculate scores from current responses"""
        from app import get_enhanced_framework, calculate_progress, get_maturity_level
        import json
        
        framework = get_enhanced_framework()
        responses = st.session_state.responses
        
        total_score = 0
        max_score = 0
        domain_scores = {}
        
        for domain_id, domain_data in framework['domains'].items():
            domain_score = 0
            domain_max = 0
            
            for question in domain_data['questions']:
                question_max = max(level['score'] for level in question['maturity_levels'])
                domain_max += question_max
                
                if question['id'] in responses and responses[question['id']] is not None:
                    domain_score += responses[question['id']]
            
            domain_percentage = (domain_score / domain_max * 100) if domain_max > 0 else 0
            domain_scores[domain_id] = {
                'name': domain_data['name'],
                'icon': domain_data.get('icon', '📊'),
                'raw_percentage': domain_percentage,
                'score': domain_score,
                'max_score': domain_max,
                'maturity_level': get_maturity_level(domain_percentage)
            }
            
            total_score += domain_score
            max_score += domain_max
        
        overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
        answered, total = calculate_progress()
        
        return {
            'overall': {
                'percentage': overall_percentage,
                'maturity_level': get_maturity_level(overall_percentage),
                'questions_answered': answered,
                'total_questions': total,
                'industry_benchmark': 65
            },
            'domains': domain_scores,
            'responses': responses
        }

# Global user data manager instance
try:
    user_data_manager = UserDataManager()
except Exception as e:
    print(f"Failed to initialize user data manager: {e}")
    user_data_manager = None