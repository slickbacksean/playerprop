import pyotp
import logging
from typing import Optional
from datetime import datetime, timedelta

class TwoFactorAuth:
    """
    Comprehensive two-factor authentication implementation.
    """
    
    @staticmethod
    def generate_totp_secret() -> str:
        """
        Generate a new TOTP secret for two-factor authentication.
        
        Returns:
            str: Base32 encoded secret
        """
        return pyotp.random_base32()

    @classmethod
    def generate_provisioning_uri(
        username: str, 
        secret: str, 
        issuer_name: str = "SportsPropPredictor"
    ) -> str:
        """
        Generate a provisioning URI for QR code generation.
        
        Args:
            username (str): User's email or username
            secret (str): TOTP secret
            issuer_name (str): Name of the service
        
        Returns:
            str: Provisioning URI for QR code
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=username, issuer_name=issuer_name)

    @classmethod
    def verify_totp(cls, secret: str, user_code: str, window: int = 1) -> bool:
        """
        Verify TOTP code from user.
        
        Args:
            secret (str): User's TOTP secret
            user_code (str): Code entered by user
            window (int): Number of timesteps to check around current time
        
        Returns:
            bool: True if code is valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(user_code, valid_window=window)
        except Exception as e:
            logging.error(f"TOTP verification failed: {e}")
            return False

    @classmethod
    def generate_backup_codes(cls, num_codes: int = 5, valid_days: int = 30) -> list:
        """
        Generate backup recovery codes.
        
        Args:
            num_codes (int): Number of backup codes to generate
            valid_days (int): Days until codes expire
        
        Returns:
            list of backup codes with expiration
        """
        backup_codes = []
        expiration = datetime.now() + timedelta(days=valid_days)
        
        for _ in range(num_codes):
            # Generate a secure 8-character code
            code = pyotp.random_base32()[:8]
            backup_codes.append({
                'code': code,
                'used': False,
                'expires_at': expiration
            })
        
        return backup_codes