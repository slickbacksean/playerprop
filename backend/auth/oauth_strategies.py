import logging
from typing import Dict, Optional
from authlib.integrations.requests_client import OAuth2Session
from authlib.common.security import generate_token

class OAuthStrategies:
    """
    Centralized OAuth authentication strategies for multiple providers.
    """
    
    @staticmethod
    def get_google_oauth_flow(client_id: str, client_secret: str, redirect_uri: str):
        """
        Configure OAuth 2.0 flow for Google authentication.
        
        Args:
            client_id (str): Google OAuth client ID
            client_secret (str): Google OAuth client secret
            redirect_uri (str): Callback URI
        
        Returns:
            OAuth2Session configured for Google
        """
        return OAuth2Session(
            client_id,
            client_secret,
            scope='openid email profile',
            redirect_uri=redirect_uri
        )

    @staticmethod
    def get_github_oauth_flow(client_id: str, client_secret: str, redirect_uri: str):
        """
        Configure OAuth 2.0 flow for GitHub authentication.
        
        Args:
            client_id (str): GitHub OAuth client ID
            client_secret (str): GitHub OAuth client secret
            redirect_uri (str): Callback URI
        
        Returns:
            OAuth2Session configured for GitHub
        """
        return OAuth2Session(
            client_id,
            client_secret,
            scope='user:email',
            redirect_uri=redirect_uri
        )

    @classmethod
    def exchange_authorization_code(
        cls, 
        oauth_session: OAuth2Session, 
        authorization_response: str
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            oauth_session (OAuth2Session): Configured OAuth session
            authorization_response (str): Authorization response URL
        
        Returns:
            Dict containing token and user information
        """
        try:
            token = oauth_session.fetch_token(
                authorization_response=authorization_response
            )
            
            # Fetch user profile
            user_info = oauth_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
            
            return {
                'token': token,
                'user_info': user_info
            }
        except Exception as e:
            logging.error(f"OAuth token exchange failed: {e}")
            raise

    @staticmethod
    def generate_state_token() -> str:
        """
        Generate a secure state token to prevent CSRF attacks.
        
        Returns:
            str: Cryptographically secure state token
        """
        return generate_token()