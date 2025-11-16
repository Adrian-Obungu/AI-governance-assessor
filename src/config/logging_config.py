"""
Structured logging configuration for AI Governance Pro
Implements audit trail and operational logging
"""
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(log_dir="logs"):
    """Initialize logging system with file and console handlers"""
    
    # Create logs directory
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger("ai_governance")
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler - INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler - DEBUG level (detailed logs)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Audit logger - tracks sensitive operations
    audit_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'audit.log'),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=12
    )
    audit_handler.setLevel(logging.INFO)
    audit_formatter = logging.Formatter(
        '%(asctime)s - AUDIT - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    audit_handler.setFormatter(audit_formatter)
    
    # Create audit logger
    audit_logger = logging.getLogger("ai_governance.audit")
    audit_logger.setLevel(logging.INFO)
    audit_logger.addHandler(audit_handler)
    
    # Security logger
    security_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'security.log'),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=12
    )
    security_handler.setLevel(logging.WARNING)
    security_formatter = logging.Formatter(
        '%(asctime)s - SECURITY - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    security_handler.setFormatter(security_formatter)
    
    security_logger = logging.getLogger("ai_governance.security")
    security_logger.setLevel(logging.WARNING)
    security_logger.addHandler(security_handler)
    
    return {
        'app': logger,
        'audit': audit_logger,
        'security': security_logger
    }

# Initialize on module import
loggers = setup_logging()
