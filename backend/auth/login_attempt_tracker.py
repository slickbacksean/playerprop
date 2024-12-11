import logging
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict

class LoginAttemptTracker:
    """
    Robust login attempt tracking and security mechanism.
    """
    
    _login_attempts = defaultdict(list)
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)

    @classmethod
    def record_login_attempt(cls, username: str, success: bool = False):
        """
        Record a login attempt for a specific user.
        
        Args:
            username (str): Username attempting login
            success (bool): Whether login was successful
        """
        current_time = datetime.now()
        
        # Clean up old attempts
        cls._login_attempts[username] = [
            attempt for attempt in cls._login_attempts[username]
            if current_time - attempt['timestamp'] < cls.LOCKOUT_DURATION
        ]
        
        # Record new attempt
        cls._login_attempts[username].append({
            'timestamp': current_time,
            'success': success
        })
        
        # Log for security tracking
        log_message = (
            f"Login attempt for {username}: " + 
            ("Successful" if success else "Failed")
        )
        logging.info(log_message)

    @classmethod
    def is_account_locked(cls, username: str) -> bool:
        """
        Check if an account is currently locked due to multiple failed attempts.
        
        Args:
            username (str): Username to check
        
        Returns:
            bool: True if account is locked, False otherwise
        """
        current_time = datetime.now()
        failed_attempts = [
            attempt for attempt in cls._login_attempts[username]
            if not attempt['success'] and 
            current_time - attempt['timestamp'] < cls.LOCKOUT_DURATION
        ]
        
        return len(failed_attempts) >= cls.MAX_ATTEMPTS

    @classmethod
    def reset_login_attempts(cls, username: str):
        """
        Reset login attempts for a specific user.
        
        Args:
            username (str): Username to reset
        """
        if username in cls._login_attempts:
            del cls._login_attempts[username]
        
        logging.info(f"Login attempts reset for {username}")