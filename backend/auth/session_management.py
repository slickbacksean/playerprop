import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from threading import Lock

class SessionManager:
    """
    Advanced session management with security features.
    """
    
    _sessions: Dict[str, Dict[str, Any]] = {}
    _session_lock = Lock()
    
    # Session configuration
    SESSION_TIMEOUT = timedelta(hours=2)
    MAX_CONCURRENT_SESSIONS = 3
    
    @classmethod
    def create_session(cls, user_id: str, additional_data: Optional[Dict] = None) -> str:
        """
        Create a new secure session for a user.
        
        Args:
            user_id (str): Unique user identifier
            additional_data (dict, optional): Extra session metadata
        
        Returns:
            str: Unique session token
        """
        with cls._session_lock:
            # Cleanup existing sessions
            cls._cleanup_expired_sessions(user_id)
            
            # Check concurrent session limit
            user_sessions = [
                sid for sid, session in cls._sessions.items() 
                if session['user_id'] == user_id
            ]
            if len(user_sessions) >= cls.MAX_CONCURRENT_SESSIONS:
                # Remove oldest session
                oldest_session = min(
                    user_sessions, 
                    key=lambda sid: cls._sessions[sid]['created_at']
                )
                del cls._sessions[oldest_session]
            
            # Generate new session
            session_token = str(uuid.uuid4())
            session_data = {
                'user_id': user_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'ip_address': None,  # Should be set during session creation
                'additional_data': additional_data or {}
            }
            
            cls._sessions[session_token] = session_data
            
            logging.info(f"New session created for user {user_id}")
            return session_token
    
    @classmethod
    def validate_session(cls, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate an existing session.
        
        Args:
            session_token (str): Session token to validate
        
        Returns:
            Dict with session data if valid, None otherwise
        """
        with cls._session_lock:
            session = cls._sessions.get(session_token)
            
            if not session:
                return None
            
            # Check session timeout
            if datetime.now() - session['created_at'] > cls.SESSION_TIMEOUT:
                cls._invalidate_session(session_token)
                return None
            
            # Update last activity
            session['last_activity'] = datetime.now()
            return session
    
    @classmethod
    def _cleanup_expired_sessions(cls, user_id: Optional[str] = None):
        """
        Remove expired sessions.
        
        Args:
            user_id (str, optional): Specific user to cleanup sessions for
        """
        now = datetime.now()
        expired_sessions = [
            token for token, session in cls._sessions.items()
            if (now - session['created_at'] > cls.SESSION_TIMEOUT) and 
               (user_id is None or session['user_id'] == user_id)
        ]
        
        for token in expired_sessions:
            del cls._sessions[token]
    
    @classmethod
    def _invalidate_session(cls, session_token: str):
        """
        Forcibly invalidate a specific session.
        
        Args:
            session_token (str): Session to invalidate
        """
        with cls._session_lock:
            if session_token in cls._sessions:
                del cls._sessions[session_token]
                logging.info(f"Session {session_token} invalidated")
    
    @classmethod
    def get_active_sessions(cls, user_id: str) -> int:
        """
        Get number of active sessions for a user.
        
        Args:
            user_id (str): User to check
        
        Returns:
            int: Number of active sessions
        """
        return sum(1 for session in cls._sessions.values() if session['user_id'] == user_id)