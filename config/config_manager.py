import os
import yaml
from typing import Dict, Any
from functools import lru_cache
from dotenv import load_dotenv

class ConfigurationManager:
    """
    Manages application configuration with environment-specific settings
    and secure secret loading.
    """
    
    def __init__(self, env: str = 'development'):
        """
        Initialize configuration manager for a specific environment.
        
        Args:
            env (str): Environment name (development/production). Defaults to 'development'.
        """
        self.env = env
        self._load_env_files()
    
    def _load_env_files(self):
        """
        Load environment-specific .env files securely.
        """
        env_path = f'config/secrets/.env.{self.env}'
        load_dotenv(dotenv_path=env_path, override=True)
    
    @lru_cache(maxsize=1)
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration, merging base and environment-specific settings.
        
        Returns:
            Dict[str, Any]: Merged configuration dictionary
        """
        try:
            # Load base configuration
            with open('config/settings/base.yml', 'r') as base_file:
                base_config = yaml.safe_load(base_file)
            
            # Load environment-specific configuration
            env_config_path = f'config/settings/{self.env}.yml'
            with open(env_config_path, 'r') as env_file:
                env_config = yaml.safe_load(env_file)
            
            # Deep merge configurations
            return self._deep_merge(base_config, env_config)
        
        except FileNotFoundError as e:
            raise ConfigurationError(f"Configuration file not found: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML configuration: {e}")
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries.
        
        Args:
            base (Dict): Base configuration dictionary
            update (Dict): Environment-specific configuration dictionary
        
        Returns:
            Dict: Merged configuration dictionary
        """
        for key, value in update.items():
            if isinstance(value, dict):
                base[key] = self._deep_merge(base.get(key, {}), value)
            else:
                base[key] = value
        return base
    
    def get(self, key: str, default=None):
        """
        Retrieve a specific configuration value.
        
        Args:
            key (str): Dot-separated configuration key
            default: Default value if key is not found
        
        Returns:
            Configuration value or default
        """
        config = self.load_config()
        keys = key.split('.')
        
        for k in keys:
            config = config.get(k, {})
            if not isinstance(config, dict):
                return config if config is not None else default
        
        return config or default

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

# Example usage
def main():
    # Development configuration
    dev_config = ConfigurationManager('development')
    print(dev_config.get('application.name'))
    print(dev_config.get('database.host'))
    
    # Production configuration
    prod_config = ConfigurationManager('production')
    print(prod_config.get('application.name'))
    print(prod_config.get('security.rate_limiting.requests_per_minute'))

if __name__ == '__main__':
    main()