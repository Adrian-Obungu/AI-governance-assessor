"""
Audit logging utilities for compliance and security tracking
"""
import logging
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any

audit_logger = logging.getLogger("ai_governance.audit")
security_logger = logging.getLogger("ai_governance.security")

class AuditLogger:
    """Centralized audit trail management"""
    
    DB_PATH = "data/governance_assessments.db"
    
    @staticmethod
    def log_authentication(email: str, success: bool, ip_address: str = None, user_agent: str = None):
        """Log authentication attempt"""
        status = "SUCCESS" if success else "FAILED"
        message = f"Authentication {status} - Email: {email}"
        
        if not success:
            security_logger.warning(message)
        else:
            audit_logger.info(message)
        
        AuditLogger._save_to_db(
            user_id=None,
            action='authentication',
            resource_type='user',
            resource_id=email,
            ip_address=ip_address,
            user_agent=user_agent,
            details=json.dumps({'success': success})
        )
    
    @staticmethod
    def log_assessment_submission(user_id: int, assessment_id: int, overall_score: float, framework: str):
        """Log assessment submission"""
        message = f"Assessment submitted - ID: {assessment_id}, User: {user_id}, Score: {overall_score}%, Framework: {framework}"
        audit_logger.info(message)
        
        AuditLogger._save_to_db(
            user_id=user_id,
            action='assessment_submitted',
            resource_type='assessment',
            resource_id=str(assessment_id),
            details=json.dumps({'score': overall_score, 'framework': framework})
        )
    
    @staticmethod
    def log_data_export(user_id: int, export_format: str, assessment_id: int, success: bool):
        """Log data export operations"""
        status = "SUCCESS" if success else "FAILED"
        message = f"Data export {status} - Format: {export_format}, Assessment: {assessment_id}, User: {user_id}"
        audit_logger.info(message)
        
        AuditLogger._save_to_db(
            user_id=user_id,
            action='data_export',
            resource_type='assessment',
            resource_id=str(assessment_id),
            details=json.dumps({'format': export_format, 'success': success})
        )
    
    @staticmethod
    def log_user_registration(email: str, organization: str, ip_address: str = None):
        """Log new user registration"""
        message = f"User registration - Email: {email}, Organization: {organization}"
        audit_logger.info(message)
        
        AuditLogger._save_to_db(
            user_id=None,
            action='user_registration',
            resource_type='user',
            resource_id=email,
            ip_address=ip_address,
            details=json.dumps({'organization': organization})
        )
    
    @staticmethod
    def log_security_event(event_type: str, severity: str, details: Dict[str, Any], user_id: Optional[int] = None):
        """Log security-related events"""
        message = f"Security Event - Type: {event_type}, Severity: {severity}, Details: {json.dumps(details)}"
        
        if severity == "critical":
            security_logger.critical(message)
        elif severity == "warning":
            security_logger.warning(message)
        else:
            security_logger.info(message)
        
        AuditLogger._save_to_db(
            user_id=user_id,
            action=f"security_{event_type}",
            resource_type='security',
            resource_id=severity,
            details=json.dumps(details)
        )
    
    @staticmethod
    def _save_to_db(user_id: Optional[int], action: str, resource_type: str, 
                   resource_id: str, ip_address: str = None, user_agent: str = None, details: str = None):
        """Save audit log to database"""
        try:
            conn = sqlite3.connect(AuditLogger.DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_logs (user_id, action, resource_type, resource_id, ip_address, user_agent, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, action, resource_type, resource_id, ip_address, user_agent, details))
            
            conn.commit()
            conn.close()
        except Exception as e:
            audit_logger.error(f"Failed to save audit log: {str(e)}")
    
    @staticmethod
    def get_audit_trail(user_id: Optional[int] = None, days: int = 90) -> list:
        """Retrieve audit trail with optional filtering"""
        try:
            conn = sqlite3.connect(AuditLogger.DB_PATH)
            cursor = conn.cursor()
            
            query = "SELECT * FROM audit_logs WHERE timestamp > datetime('now', '-" + str(days) + " days')"
            params = []
            
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            
            query += " ORDER BY timestamp DESC"
            
            cursor.execute(query, params)
            logs = cursor.fetchall()
            conn.close()
            
            return logs
        except Exception as e:
            audit_logger.error(f"Failed to retrieve audit trail: {str(e)}")
            return []
