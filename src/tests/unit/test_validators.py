"""
Unit tests for authentication and security modules
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from modules.utils.validators import Validators


class TestValidators:
    """Test input validators"""
    
    def test_email_validation_valid(self):
        """Test valid email addresses"""
        validator = Validators()
        
        valid_emails = [
            "user@example.com",
            "test.user@example.co.uk",
            "user+tag@example.com"
        ]
        
        for email in valid_emails:
            is_valid, msg = validator.validate_email(email)
            assert is_valid, f"Email {email} should be valid, got error: {msg}"
    
    def test_email_validation_invalid(self):
        """Test invalid email addresses"""
        validator = Validators()
        
        invalid_emails = [
            "notanemail",
            "user@",
            "@example.com",
            "user@.com",
            ""
        ]
        
        for email in invalid_emails:
            is_valid, msg = validator.validate_email(email)
            assert not is_valid, f"Email {email} should be invalid"
    
    def test_password_validation_strong(self):
        """Test strong password validation"""
        validator = Validators()
        
        strong_passwords = [
            "MyPassword123!@#",
            "SecurePass$2024",
            "Test@Password123"
        ]
        
        for password in strong_passwords:
            is_valid, msg = validator.validate_password(password)
            assert is_valid, f"Password should be valid, got error: {msg}"
    
    def test_password_validation_weak(self):
        """Test weak password validation"""
        validator = Validators()
        
        weak_passwords = [
            "short",  # Too short
            "NoSpecialChar123",  # Missing special char
            "password123!",  # Missing uppercase
            "PASSWORD123!",  # Missing lowercase
            "Pass!",  # Too short
        ]
        
        for password in weak_passwords:
            is_valid, msg = validator.validate_password(password)
            assert not is_valid, f"Password '{password}' should be invalid"
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        validator = Validators()
        
        # Test XSS prevention
        xss_input = "<script>alert('xss')</script>"
        sanitized = validator.sanitize_input(xss_input)
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized
    
    def test_assessment_response_validation(self):
        """Test assessment response validation"""
        validator = Validators()
        
        # Valid scores
        for score in [0, 1, 2, 3, 4, 5]:
            is_valid, msg = validator.validate_assessment_response(score, "Q1")
            assert is_valid, f"Score {score} should be valid"
        
        # Invalid scores
        for score in [-1, 6, 10, 100]:
            is_valid, msg = validator.validate_assessment_response(score, "Q1")
            assert not is_valid, f"Score {score} should be invalid"
    
    def test_file_upload_validation(self):
        """Test file upload validation"""
        validator = Validators()
        
        # Valid file
        is_valid, msg = validator.validate_file_upload(
            "document.pdf",
            5 * 1024 * 1024,  # 5MB
            allowed_types=['application/pdf']
        )
        assert is_valid
        
        # File too large
        is_valid, msg = validator.validate_file_upload(
            "large.pdf",
            15 * 1024 * 1024,  # 15MB (exceeds 10MB limit)
        )
        assert not is_valid
        
        # Path traversal attempt
        is_valid, msg = validator.validate_file_upload(
            "../../../etc/passwd",
            100
        )
        assert not is_valid


class TestPasswordStrengthRequirements:
    """Test NIST SP 800-63B password requirements"""
    
    def test_minimum_length_requirement(self):
        """Test minimum length of 12 characters"""
        validator = Validators()
        
        # Too short
        is_valid, _ = validator.validate_password("Short1!")
        assert not is_valid
        
        # Exactly 12 characters (should be valid with other requirements met)
        is_valid, _ = validator.validate_password("Valid1Pass$!")
        assert is_valid
    
    def test_uppercase_requirement(self):
        """Test uppercase letter requirement"""
        validator = Validators()
        
        is_valid, msg = validator.validate_password("password123!@#")
        assert not is_valid
        assert "uppercase" in msg.lower()
    
    def test_lowercase_requirement(self):
        """Test lowercase letter requirement"""
        validator = Validators()
        
        is_valid, msg = validator.validate_password("PASSWORD123!@#")
        assert not is_valid
        assert "lowercase" in msg.lower()
    
    def test_digit_requirement(self):
        """Test digit requirement"""
        validator = Validators()
        
        is_valid, msg = validator.validate_password("Password!@#abc")
        assert not is_valid
        assert "digit" in msg.lower()
    
    def test_special_character_requirement(self):
        """Test special character requirement"""
        validator = Validators()
        
        is_valid, msg = validator.validate_password("Password123abc")
        assert not is_valid
        assert "special" in msg.lower()


class TestXSSPrevention:
    """Test XSS prevention in input sanitization"""
    
    def test_script_tag_escaping(self):
        """Test that script tags are escaped"""
        validator = Validators()
        
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "<svg onload=alert('xss')>",
            "javascript:alert('xss')"
        ]
        
        for payload in xss_payloads:
            sanitized = validator.sanitize_input(payload)
            assert "<" not in sanitized or "&lt;" in sanitized
            assert ">" not in sanitized or "&gt;" in sanitized


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
