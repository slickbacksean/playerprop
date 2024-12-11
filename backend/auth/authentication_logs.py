import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from typing import Dict, Optional

class AuthenticationLogger:
    """
    Comprehensive authentication and security event logging system.
    """
    
    @staticmethod
    def setup_logger(log_dir: str = 'logs') -> logging.Logger:
        """
        Set up a rotating file logger for authentication events.
        
        Args:
            log_dir (str): Directory to store log files
        
        Returns:
            logging.Logger: Configured logger
        """
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Log file with timestamp
        log_file = os.path.join(log_dir, f'auth_{datetime.now().strftime("%Y%m%d")}.log')
        
        # Create logger
        logger = logging.getLogger('auth_logger')
        logger.setLevel(logging.INFO)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler if not already added
        if not logger.handlers:
            logger.addHandler(file_handler)
        
        return logger
    
    @classmethod
    def log_login_attempt(
        cls, 
        username: str, 
        success: bool, 
        ip_address: Optional[str] = None,
        additional_info: Optional[Dict] = None
    ):
        """
        Log a login attempt with comprehensive details.
        
        Args:
            username (str): Username attempting login
            success (bool): Whether login was successful
            ip_address (str, optional): IP address of login attempt
            additional_info (dict, optional): Extra contextual information
        """
        logger = cls.setup_logger()
        
        log_data = {
            'username': username,
            'status': 'SUCCESS' if success else 'FAILED',
            'ip_address': ip_address or 'UNKNOWN'
        }
        
        if additional_info:
            log_data.update(additional_info)
        
        log_message = ' | '.join(f'{k}={v}' for k, v in log_data.items())
        
        if success:
            logger.info(f"LOGIN_SUCCESS: {log_message}")
        else:
            logger.warning(f"LOGIN_FAILED: {log_message}")
    
    @classmethod
    def log_security_event(
        cls, 
        event_type: str, 
        username: str, 
        details: Optional[Dict] = None
    ):
        """
        Log various security-related events.
        
        Args:
            event_type (str): Type of security event
            username (str): User associated with event
            details (dict, optional): Additional event details
        """
        logger = cls.setup_logger()
        
        log_data = {
            'username': username,
            'event_type': event_type
        }
        
        if details:
            log_data.update(details)
        
        log_message = ' | '.join(f'{k}={v}' for k, v in log_data.items())
        
        logger.info(