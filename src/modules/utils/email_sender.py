"""Pluggable email sender with SMTP and console fallback."""
from typing import Tuple, Optional
import smtplib
from email.message import EmailMessage
import logging
import sys
import os

# Handle import paths - support both direct and relative imports
try:
    from config.config import Config
except ImportError:
    try:
        # Add src to path for relative imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
        from src.config.config import Config
    except ImportError:
        # Fallback: create minimal config if import fails
        class Config:
            SMTP_ENABLED = os.getenv('SMTP_ENABLED', 'false').lower() == 'true'
            SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
            SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
            SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
            SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
            EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@governance-assessor.com')


logger = logging.getLogger(__name__)


def send_email_smtp(to_email: str, subject: str, body: str) -> Tuple[bool, Optional[str]]:
    """Send email via SMTP using settings in Config. Returns (True, None) on success or (False, error)."""
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = Config.EMAIL_FROM
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            if Config.SMTP_USERNAME and Config.SMTP_PASSWORD:
                smtp.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            smtp.send_message(msg)
        return True, None
    except Exception as e:
        logger.exception("Failed to send email via SMTP")
        return False, str(e)


def send_reset_email(to_email: str, token: str) -> Tuple[bool, Optional[str]]:
    """Compose and send a password reset email with the token."""
    subject = "AI Governance Pro - Password Reset"
    reset_instructions = (
        f"You requested a password reset for your AI Governance Pro account.\n\n"
        f"Use the following secure token to reset your password (expires in {60} minutes):\n\n"
        f"{token}\n\n"
        "If you did not request this, please ignore this email."
    )

    if Config.SMTP_ENABLED:
        return send_email_smtp(to_email, subject, reset_instructions)

    # Fallback: log and return token to caller
    logger.info("SMTP not enabled; password reset token generated (console fallback)")
    logger.info(f"Password reset token for {to_email}: {token}")
    return True, None
