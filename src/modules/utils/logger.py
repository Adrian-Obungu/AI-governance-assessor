"""
Structured logging system for AI Governance Pro
Provides centralized audit trail and monitoring
"""
import logging
import logging.handlers
import json
from datetime import datetime
import os
from pathlib import Path


class StructuredLogger:
    """Structured logging with JSON audit trails"""
    
    def __init__(self, name: str, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging handlers and formatters"""
        # Create logs directory if it doesn't exist
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Set logger level
        self.logger.setLevel(logging.DEBUG)
        
        # File handler - rotating logs
        log_file = os.path.join(self.log_dir, "app.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Audit handler - JSON structured logs
        audit_file = os.path.join(self.log_dir, "audit.json")
        audit_handler = logging.handlers.RotatingFileHandler(
            audit_file,
            maxBytes=50 * 1024 * 1024,  # 50MB
            backupCount=20
        )
        audit_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        json_formatter = logging.Formatter(
            '%(message)s'
        )
        
        file_handler.setFormatter(detailed_formatter)
        audit_handler.setFormatter(json_formatter)
        console_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(audit_handler)
        self.logger.addHandler(console_handler)
    
    def log_authentication(self, event_type: str, email: str, success: bool, 
                          ip_address: str = None, details: str = None):
        """Log authentication events to audit trail"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'authentication',
            'event_subtype': event_type,
            'email': email,
            'success': success,
            'ip_address': ip_address,
            'details': details
        }
        self.logger.info(json.dumps(audit_log))
    
    def log_assessment_submitted(self, user_id: int, assessment_id: int,
                                 overall_score: float, maturity_level: str,
                                 ip_address: str = None):
        """Log assessment submission to audit trail"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'assessment',
            'event_subtype': 'submitted',
            'user_id': user_id,
            'assessment_id': assessment_id,
            'overall_score': overall_score,
            'maturity_level': maturity_level,
            'ip_address': ip_address
        }
        self.logger.info(json.dumps(audit_log))
    
    def log_export_operation(self, user_id: int, export_format: str,
                            success: bool, filename: str = None,
                            ip_address: str = None, error: str = None):
        """Log data export operations to audit trail"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'export',
            'user_id': user_id,
            'format': export_format,
            'success': success,
            'filename': filename,
            'ip_address': ip_address,
            'error': error
        }
        self.logger.info(json.dumps(audit_log))
    
    def log_data_access(self, user_id: int, resource_type: str,
                       resource_id: str, action: str, ip_address: str = None):
        """Log data access for compliance"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'data_access',
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'ip_address': ip_address
        }
        self.logger.info(json.dumps(audit_log))
    
    def log_security_event(self, event_type: str, severity: str,
                          description: str, ip_address: str = None,
                          user_id: int = None):
        """Log security events"""
        audit_log = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'security',
            'security_event_type': event_type,
            'severity': severity,
            'description': description,
            'user_id': user_id,
            'ip_address': ip_address
        }
        self.logger.warning(json.dumps(audit_log))
    
    def log_error(self, error_type: str, error_message: str,
                 context: str = None, user_id: int = None):
        """Log application errors"""
        self.logger.error(
            f"{error_type}: {error_message}",
            extra={'context': context, 'user_id': user_id}
        )


# Global logger instances
app_logger = StructuredLogger("ai_governance_app")
auth_logger = StructuredLogger("ai_governance_auth")
assessment_logger = StructuredLogger("ai_governance_assessment")
export_logger = StructuredLogger("ai_governance_export")
security_logger = StructuredLogger("ai_governance_security")
