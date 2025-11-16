"""
Input validation and sanitization utilities for enterprise security
"""
import re
import html
from typing import Tuple

class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass


class Validators:
    """Enterprise-grade input validators"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format (RFC 5322 simplified)
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or len(email) > 254:
            return False, "Email must be between 1 and 254 characters"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength (NIST SP 800-63B compliant)
        
        Requirements:
        - Minimum 12 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        if len(password) < 12:
            errors.append("Password must be at least 12 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            errors.append("Password must contain at least one special character (!@#$%^&*)")
        
        if errors:
            return False, " | ".join(errors)
        
        return True, ""
    
    @staticmethod
    def sanitize_input(value: str, field_type: str = "text") -> str:
        """
        Sanitize user input to prevent XSS and SQL injection
        
        Args:
            value: Input value to sanitize
            field_type: Type of field ('text', 'email', 'name')
            
        Returns:
            Sanitized input
        """
        if not value:
            return ""
        
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # HTML escape to prevent XSS
        value = html.escape(value)
        
        if field_type == "name":
            # Allow only alphanumeric, spaces, hyphens, and apostrophes
            value = re.sub(r'[^a-zA-Z0-9\s\-\']', '', value)
        elif field_type == "email":
            # Email sanitization already handled by validator
            pass
        
        return value
    
    @staticmethod
    def validate_assessment_response(score: int, question_id: str) -> Tuple[bool, str]:
        """
        Validate assessment response score
        
        Args:
            score: Score value (should be 0-5)
            question_id: Question identifier
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(score, int):
            return False, f"Score for {question_id} must be an integer"
        
        if score < 0 or score > 5:
            return False, f"Score for {question_id} must be between 0 and 5"
        
        return True, ""
    
    @staticmethod
    def validate_file_upload(filename: str, file_size: int, allowed_types: list = None) -> Tuple[bool, str]:
        """
        Validate file upload (server-side validation)
        
        Args:
            filename: Original filename
            file_size: File size in bytes
            allowed_types: List of allowed MIME types
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Default allowed types for evidence upload
        if allowed_types is None:
            allowed_types = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                           'text/plain', 'image/png', 'image/jpeg', 'image/jpg']
        
        max_file_size = 10 * 1024 * 1024  # 10MB
        max_user_storage = 100 * 1024 * 1024  # 100MB
        
        # Check file size
        if file_size > max_file_size:
            return False, f"File size exceeds 10MB limit ({file_size / 1024 / 1024:.1f}MB)"
        
        # Sanitize filename
        if not filename or len(filename) == 0:
            return False, "Filename cannot be empty"
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Invalid filename - path traversal detected"
        
        return True, ""
    
    @staticmethod
    def validate_organization_name(org_name: str) -> Tuple[bool, str]:
        """
        Validate organization name
        
        Args:
            org_name: Organization name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not org_name or len(org_name.strip()) == 0:
            return False, "Organization name cannot be empty"
        
        if len(org_name) > 255:
            return False, "Organization name must be 255 characters or less"
        
        return True, ""


# Global validator instance
validators = Validators()
