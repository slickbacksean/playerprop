import bcrypt
import re
import logging
from typing import Optional, Dict
from secrets import token_hex

class PasswordUtils:
    """
    Comprehensive password utility functions for secure password management.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt with secure defaults.
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        try:
            # Generate a salt and hash the password
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logging.error(f"Password hashing failed: {e}")
            raise

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password (str): Password to verify
            hashed_password (str): Previously hashed password
        
        Returns:
            bool: True if password is correct, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logging.error(f"Password verification failed: {e}")
            return False

    @staticmethod
    def generate_reset_token() -> str:
        """
        Generate a secure password reset token.
        
        Returns:
            str: Cryptographically secure reset token
        """
        return token_hex(32)  # 64 character hex token

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, bool]:
        """
        Validate password strength against multiple criteria.
        
        Args:
            password (str): Password to validate
        
        Returns:
            Dict containing validation results
        """
        validation_results = {
            'length': len(password) >= 12,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'\d', password)),
            'special_char': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        validation_results['overall'] = all(validation_results.values())
        return validation_results

    @staticmethod
    def password_meets_complexity(password: str) -> bool:
        """
        Check if password meets all complexity requirements.
        
        Args:
            password (str): Password to check
        
        Returns:
            bool: True if password is sufficiently complex
        """
        validation = PasswordUtils.validate_password_strength(password)
        return validation['overall']