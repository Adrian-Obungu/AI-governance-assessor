"""
Configuration management for AI Governance Pro
Centralizes all configuration with environment-based overrides
"""
import os
from typing import Optional
import logging

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, proceed without .env support
    pass

logger = logging.getLogger(__name__)


class Config:
    """Central configuration class for the application"""
    
    # Application
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "data/governance_assessments.db")
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
    
    # Password Policy
    PASSWORD_MIN_LENGTH = int(os.getenv("PASSWORD_MIN_LENGTH", "12"))
    PASSWORD_REQUIRE_UPPERCASE = os.getenv("PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_LOWERCASE = os.getenv("PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true"
    PASSWORD_REQUIRE_DIGIT = os.getenv("PASSWORD_REQUIRE_DIGIT", "true").lower() == "true"
    PASSWORD_REQUIRE_SPECIAL = os.getenv("PASSWORD_REQUIRE_SPECIAL", "true").lower() == "true"
    PASSWORD_HISTORY_COUNT = int(os.getenv("PASSWORD_HISTORY_COUNT", "5"))
    
    # Account Lockout
    LOGIN_MAX_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS", "5"))
    LOGIN_LOCKOUT_MINUTES = int(os.getenv("LOGIN_LOCKOUT_MINUTES", "30"))
    
    # Session
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))
    SESSION_TIMEOUT_ABSOLUTE_MINUTES = int(os.getenv("SESSION_TIMEOUT_ABSOLUTE_MINUTES", "480"))
    MAX_CONCURRENT_SESSIONS = int(os.getenv("MAX_CONCURRENT_SESSIONS", "3"))
    
    # Encryption
    ENCRYPTION_ENABLED = os.getenv("ENCRYPTION_ENABLED", "true").lower() == "true"
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    ENCRYPT_PII_FIELDS = os.getenv("ENCRYPT_PII_FIELDS", "true").lower() == "true"
    
    # Streamlit
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_ADDRESS = os.getenv("STREAMLIT_ADDRESS", "0.0.0.0")
    STREAMLIT_HEADLESS = os.getenv("STREAMLIT_HEADLESS", "true").lower() == "true"
    STREAMLIT_LOGGER_LEVEL = os.getenv("STREAMLIT_LOGGER_LEVEL", "info")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "10"))
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json")
    AUDIT_LOG_ENABLED = os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true"
    
    # Monitoring
    PROMETHEUS_ENABLED = os.getenv("PROMETHEUS_ENABLED", "false").lower() == "true"
    PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))
    METRICS_COLLECTION_ENABLED = os.getenv("METRICS_COLLECTION_ENABLED", "true").lower() == "true"
    APM_ENABLED = os.getenv("APM_ENABLED", "false").lower() == "true"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    AUTH_RATE_LIMIT_PER_MINUTE = int(os.getenv("AUTH_RATE_LIMIT_PER_MINUTE", "5"))
    RATE_LIMIT_BACKEND = os.getenv("RATE_LIMIT_BACKEND", "memory")
    
    # Email
    SMTP_ENABLED = os.getenv("SMTP_ENABLED", "false").lower() == "true"
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@aigovernancepro.com")
    
    # External Integrations
    VIRUS_SCAN_ENABLED = os.getenv("VIRUS_SCAN_ENABLED", "false").lower() == "true"
    CLAMAV_HOST = os.getenv("CLAMAV_HOST", "localhost")
    CLAMAV_PORT = int(os.getenv("CLAMAV_PORT", "3310"))
    
    SLACK_ENABLED = os.getenv("SLACK_ENABLED", "false").lower() == "true"
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    
    SENTRY_ENABLED = os.getenv("SENTRY_ENABLED", "false").lower() == "true"
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    
    # Compliance
    GDPR_COMPLIANCE_ENABLED = os.getenv("GDPR_COMPLIANCE_ENABLED", "true").lower() == "true"
    DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "2555"))
    REQUIRE_CONSENT = os.getenv("REQUIRE_CONSENT", "true").lower() == "true"
    PRIVACY_POLICY_URL = os.getenv("PRIVACY_POLICY_URL", "https://your-domain.com/privacy")
    TERMS_OF_SERVICE_URL = os.getenv("TERMS_OF_SERVICE_URL", "https://your-domain.com/terms")
    
    # Backup
    BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    BACKUP_FREQUENCY_HOURS = int(os.getenv("BACKUP_FREQUENCY_HOURS", "24"))
    BACKUP_RETENTION_DAYS = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))
    BACKUP_DESTINATION = os.getenv("BACKUP_DESTINATION", "/local/backup/path")
    
    # AWS
    AWS_ENABLED = os.getenv("AWS_ENABLED", "false").lower() == "true"
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")
    
    # Kubernetes/Container
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "dev")
    REPLICA_COUNT = int(os.getenv("REPLICA_COUNT", "1"))
    RESOURCE_LIMIT_MEMORY = os.getenv("RESOURCE_LIMIT_MEMORY", "512Mi")
    RESOURCE_REQUEST_MEMORY = os.getenv("RESOURCE_REQUEST_MEMORY", "256Mi")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration"""
        errors = []
        
        if cls.APP_ENV == "production":
            if cls.SECRET_KEY == "change-me-in-production":
                errors.append("SECRET_KEY must be changed in production")
            if cls.JWT_SECRET == "change-me-in-production":
                errors.append("JWT_SECRET must be changed in production")
            if cls.ENCRYPTION_ENABLED and not cls.ENCRYPTION_KEY:
                errors.append("ENCRYPTION_KEY required when ENCRYPTION_ENABLED is true")
            if cls.DEBUG:
                errors.append("DEBUG must be false in production")
        
        if cls.DATABASE_TYPE == "postgresql" and not cls.DATABASE_URL.startswith("postgresql://"):
            errors.append("Invalid PostgreSQL database URL")
        
        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            return False
        
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Return configuration as dictionary (excluding secrets)"""
        return {
            'APP_ENV': cls.APP_ENV,
            'DEBUG': cls.DEBUG,
            'DATABASE_TYPE': cls.DATABASE_TYPE,
            'ENCRYPTION_ENABLED': cls.ENCRYPTION_ENABLED,
            'RATE_LIMIT_ENABLED': cls.RATE_LIMIT_ENABLED,
            'AUDIT_LOG_ENABLED': cls.AUDIT_LOG_ENABLED,
            'GDPR_COMPLIANCE_ENABLED': cls.GDPR_COMPLIANCE_ENABLED,
        }


# Validate configuration on import
if not Config.validate():
    logger.warning("Configuration validation failed. Check settings before deployment.")
