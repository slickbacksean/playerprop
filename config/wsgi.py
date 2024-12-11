import os
import sys
import logging
from typing import Dict, Any

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wsgi_application.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WSGIConfig:
    """
    WSGI Application Configuration and Initialization
    """
    def __init__(self, config_path: str = None):
        """
        Initialize WSGI configuration with optional config path
        
        Args:
            config_path (str, optional): Path to configuration file
        """
        self.config = self._load_configuration(config_path)
        self.logger = logger
        
        try:
            self._validate_configuration()
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            raise
    
    def _load_configuration(self, config_path: str = None) -> Dict[str, Any]:
        """
        Load application configuration
        
        Args:
            config_path (str, optional): Path to configuration file
        
        Returns:
            Dict of configuration settings
        """
        try:
            import yaml
            
            # Default configuration
            default_config = {
                'application': {
                    'name': 'SportsPropPredictor',
                    'environment': 'production',
                    'debug': False,
                    'secret_key': os.environ.get('SECRET_KEY', 'development_secret_key')
                },
                'server': {
                    'host': '0.0.0.0',
                    'port': 8000,
                    'workers': 4,
                    'timeout': 120
                },
                'database': {
                    'connection_string': os.environ.get(
                        'DATABASE_URL', 
                        'postgresql://user:password@localhost/sportspropdb'
                    )
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            }
            
            # If config path provided, merge with default
            if config_path and os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    file_config = yaml.safe_load(config_file)
                    default_config.update(file_config)
            
            self.logger.info("Configuration loaded successfully")
            return default_config
        
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return default_config
    
    def _validate_configuration(self):
        """
        Validate critical configuration parameters
        """
        critical_paths = [
            'SECRET_KEY', 
            'DATABASE_URL'
        ]
        
        for path in critical_paths:
            if not os.environ.get(path):
                self.logger.warning(f"Critical environment variable {path} not set")
    
    def create_application(self):
        """
        Create and configure WSGI application
        
        Returns:
            Configured WSGI application
        """
        try:
            from flask import Flask
            from backend.database.database import initialize_database
            
            app = Flask(__name__)
            
            # Apply configuration
            app.config.update(
                SECRET_KEY=self.config['application']['secret_key'],
                DEBUG=self.config['application']['debug'],
                ENV=self.config['application']['environment']
            )
            
            # Initialize database
            initialize_database(
                connection_string=self.config['database']['connection_string']
            )
            
            # Register blueprints and extensions here
            # from backend.routes import main_blueprint
            # app.register_blueprint(main_blueprint)
            
            self.logger.info("WSGI Application created successfully")
            return app
        
        except ImportError as e:
            self.logger.error(f"Dependency import error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Application creation failed: {e}")
            raise

def application(environ, start_response):
    """
    Main WSGI application entry point
    
    Args:
        environ (dict): WSGI environment dictionary
        start_response (callable): WSGI start_response function
    
    Returns:
        Iterable of response data
    """
    try:
        wsgi_config = WSGIConfig('config/settings/wsgi_config.yml')
        app = wsgi_config.create_application()
        
        return app(environ, start_response)
    
    except Exception as e:
        logger.error(f"WSGI Application error: {e}")
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Internal Server Error']

# Gunicorn configuration
if __name__ == "__main__":
    from gunicorn.app.base import BaseApplication

    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': f"{os.environ.get('HOST', '0.0.0.0')}:{os.environ.get('PORT', 8000)}",
        'workers': 4,
        'worker_class': 'sync',
        'timeout': 120
    }

    GunicornApp(application, options).run()