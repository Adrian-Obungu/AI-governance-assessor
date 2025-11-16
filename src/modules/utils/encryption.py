"""
Data encryption module for enterprise security
Handles encryption/decryption of PII and sensitive data
"""
import logging
import os
from typing import Optional

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("cryptography package not installed. Encryption features disabled.")

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Handles PII encryption at the field level"""
    
    def __init__(self):
        """Initialize with encryption key from environment"""
        if not ENCRYPTION_AVAILABLE:
            logger.warning("cryptography not installed. Encryption disabled.")
            self.cipher = None
            return
        
        self.key = os.getenv("ENCRYPTION_KEY")
        
        if not self.key:
            logger.warning("ENCRYPTION_KEY not set in environment. Encryption disabled.")
            self.cipher = None
        else:
            try:
                # Convert key string to bytes
                self.cipher = Fernet(self.key.encode() if isinstance(self.key, str) else self.key)
                logger.info("Encryption manager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize encryption: {e}")
                self.cipher = None
    
    def encrypt(self, plaintext: str) -> Optional[str]:
        """
        Encrypt plaintext data
        
        Args:
            plaintext: Data to encrypt
            
        Returns:
            Encrypted data as string, or original if encryption disabled
        """
        if not plaintext or not self.cipher:
            return plaintext
        
        try:
            encrypted = self.cipher.encrypt(plaintext.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return plaintext
    
    def decrypt(self, encrypted_text: str) -> Optional[str]:
        """
        Decrypt encrypted data
        
        Args:
            encrypted_text: Encrypted data
            
        Returns:
            Decrypted plaintext, or original if decryption fails
        """
        if not encrypted_text or not self.cipher:
            return encrypted_text
        
        try:
            decrypted = self.cipher.decrypt(encrypted_text.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_text
    
    def encrypt_email(self, email: str) -> str:
        """Encrypt email address"""
        return self.encrypt(email)
    
    def decrypt_email(self, encrypted_email: str) -> str:
        """Decrypt email address"""
        return self.decrypt(encrypted_email)
    
    def encrypt_full_name(self, full_name: str) -> str:
        """Encrypt full name"""
        return self.encrypt(full_name)
    
    def decrypt_full_name(self, encrypted_name: str) -> str:
        """Decrypt full name"""
        return self.decrypt(encrypted_name)
    
    def encrypt_organization(self, org: str) -> str:
        """Encrypt organization name"""
        return self.encrypt(org)
    
    def decrypt_organization(self, encrypted_org: str) -> str:
        """Decrypt organization name"""
        return self.decrypt(encrypted_org)


# Global encryption manager instance
encryption_manager = EncryptionManager()
