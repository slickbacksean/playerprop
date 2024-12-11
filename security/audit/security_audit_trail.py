import logging
from datetime import datetime
import json
import uuid
import socket
import getpass
import platform
import threading
import os
import hmac
import hashlib

class SecurityAuditTrail:
    def __init__(self, audit_log_path: str = 'security_audit.log', secret_key: bytes = None):
        """
        Initialize comprehensive security audit trail logging system.
        
        Args:
            audit_log_path (str): Path to the audit log file
            secret_key (bytes): Optional secret key for log integrity verification
        """
        # Ensure log directory exists
        os.makedirs(os.path.dirname(audit_log_path), exist_ok=True)
        
        # Thread-safe logging configuration
        self._lock = threading.Lock()
        
        # Logging setup
        self.logger = logging.getLogger('SecurityAuditTrail')
        self.logger.setLevel(logging.INFO)
        
        # File handler with secure formatting
        file_handler = logging.FileHandler(audit_log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Secret key for log integrity
        self._secret_key = secret_key or os.urandom(32)

    def _generate_log_signature(self, log_data: dict) -> str:
        """
        Generate a cryptographic signature for log integrity.
        
        Args:
            log_data (dict): Log entry details
        
        Returns:
            str: HMAC signature
        """
        log_string = json.dumps(log_data, sort_keys=True)
        return hmac.new(
            self._secret_key, 
            log_string.encode(), 
            hashlib.sha256
        ).hexdigest()

    def _get_system_context(self) -> dict:
        """
        Collect comprehensive system and user context information.
        
        Returns:
            dict: Detailed system and user context
        """
        return {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'hostname': socket.gethostname(),
            'username': getpass.getuser(),
            'process_id': os.getpid(),
            'thread_id': threading.get_ident(),
            'os': {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine()
            }
        }

    def log_security_event(self, 
                            event_type: str, 
                            user_id: str = None, 
                            description: str = None, 
                            severity: str = 'INFO'):
        """
        Log comprehensive security events with detailed context.
        
        Args:
            event_type (str): Type of security event
            user_id (str, optional): User identifier
            description (str, optional): Event description
            severity (str, optional): Event severity level
        """
        with self._lock:
            log_entry = self._get_system_context()
            
            # Populate event details
            log_entry.update({
                'event_type': event_type,
                'user_id': user_id,
                'description': description,
                'severity': severity
            })
            
            # Generate log signature for integrity
            log_entry['signature'] = self._generate_log_signature(log_entry)
            
            # Log as JSON for structured parsing
            self.logger.log(
                getattr(logging, severity.upper()), 
                json.dumps(log_entry)
            )

    def log_authentication_event(self, 
                                 user_id: str, 
                                 event_type: str, 
                                 status: str, 
                                 ip_address: str = None):
        """
        Specialized logging for authentication-related events.
        
        Args:
            user_id (str): User identifier
            event_type (str): Authentication event type
            status (str): Success or failure status
            ip_address (str, optional): Source IP address
        """
        description = f"Authentication {event_type} for user {user_id}"
        severity = 'WARNING' if status == 'FAILED' else 'INFO'
        
        additional_context = {
            'authentication_status': status,
            'ip_address': ip_address
        }
        
        self.log_security_event(
            event_type=f"AUTH_{event_type}", 
            user_id=user_id, 
            description=description,
            severity=severity
        )

def main():
    # Example usage
    audit_trail = SecurityAuditTrail()
    
    # Log various security events
    audit_trail.log_security_event(
        event_type='SYSTEM_STARTUP',
        description='Application initialization'
    )
    
    audit_trail.log_authentication_event(
        user_id='user123', 
        event_type='LOGIN', 
        status='SUCCESS', 
        ip_address='192.168.1.100'
    )
    
    audit_trail.log_authentication_event(
        user_id='user456', 
        event_type='LOGIN', 
        status='FAILED', 
        ip_address='10.0.0.50'
    )

if __name__ == "__main__":
    main()