"""
Password validation and security utilities
Implements NIST SP 800-63B guidelines
"""
import re
from typing import Tuple

class PasswordValidator:
    """Comprehensive password validation"""
    
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True
    
    # Common weak passwords and patterns
    WEAK_PATTERNS = [
        r'(.)\1{2,}',  # Repeating characters
        r'(?:pass|admin|user|test|demo|1234|qwerty|123456)',  # Common words
    ]
    
    @staticmethod
    def validate(password: str) -> Tuple[bool, str]:
        """
        Validate password against security requirements
        Returns: (is_valid, error_message)
        """
        
        # Length check
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Password must be at least {PasswordValidator.MIN_LENGTH} characters long"
        
        # Uppercase check
        if PasswordValidator.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter (A-Z)"
        
        # Lowercase check
        if PasswordValidator.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter (a-z)"
        
        # Digit check
        if PasswordValidator.REQUIRE_DIGITS and not re.search(r'\d', password):
            return False, "Password must contain at least one digit (0-9)"
        
        # Special character check
        if PasswordValidator.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            return False, "Password must contain at least one special character (!@#$%^&* etc.)"
        
        # Weak pattern check
        for pattern in PasswordValidator.WEAK_PATTERNS:
            if re.search(pattern, password, re.IGNORECASE):
                return False, "Password contains common or predictable patterns"
        
        return True, "Password is valid"
    
    @staticmethod
    def get_requirements() -> dict:
        """Get password requirements for display"""
        return {
            'min_length': PasswordValidator.MIN_LENGTH,
            'uppercase': PasswordValidator.REQUIRE_UPPERCASE,
            'lowercase': PasswordValidator.REQUIRE_LOWERCASE,
            'digits': PasswordValidator.REQUIRE_DIGITS,
            'special_chars': PasswordValidator.REQUIRE_SPECIAL,
            'example': "MySecureP@ss123"
        }
