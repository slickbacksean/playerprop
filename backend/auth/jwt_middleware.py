import jwt
import time
import logging
from functools import wraps
from typing import Dict, Any, Callable
from flask import request, jsonify

class JWTMiddleware:
    """
    Comprehensive JWT authentication and authorization middleware.
    """
    
    SECRET_KEY = 'your_secure_secret_key'  # Replace with environment variable
    ALGORITHM = 'HS256'
    TOKEN_EXPIRATION = 3600  # 1 hour

    @classmethod
    def generate_token(cls, user_id: str, roles: list = None) -> str:
        """
        Generate a JWT token for a user.
        
        Args:
            user_id (str): Unique user identifier
            roles (list, optional): User roles for authorization
        
        Returns:
            str: JWT token
        """
        try:
            payload = {
                'user_id': user_id,
                'roles': roles or [],
                'exp': int(time.time()) + cls.TOKEN_EXPIRATION
            }
            return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        except Exception as e:
            logging.error(f"Token generation failed: {e}")
            raise

    @classmethod
    def decode_token(cls, token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        
        Args:
            token (str): JWT token to decode
        
        Returns:
            Dict containing token payload
        """
        try:
            return jwt.decode(
                token, 
                cls.SECRET_KEY, 
                algorithms=[cls.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired")
            raise
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            raise

    @classmethod
    def authenticate(cls, required_roles: list = None):
        """
        Decorator for authenticating routes with optional role-based access.
        
        Args:
            required_roles (list, optional): Roles allowed to access the route
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                token = request.headers.get('Authorization', '').split(' ')[-1]
                
                if not token:
                    return jsonify({"error": "No token provided"}), 401
                
                try:
                    payload = cls.decode_token(token)
                    
                    # Role-based access control
                    if required_roles:
                        if not set(required_roles).intersection(set(payload['roles'])):
                            return jsonify({"error": "Insufficient permissions"}), 403
                    
                    # Attach user context to request
                    request.user = payload
                    return func(*args, **kwargs)
                
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    return jsonify({"error": "Invalid or expired token"}), 401
            return wrapper
        return decorator