import os
import yaml
import logging
from typing import Dict, Any, Optional, Union

class ModelConfiguration:
    """
    Centralized configuration management for machine learning models in the 
    Sports Prop Predictor project.
    """
    def __init__(
        self, 
        config_path: str = 'config/model_config.yml',
        log_path: str = 'logs/model_configuration.log'
    ):
        """
        Initialize the Model Configuration manager.
        
        Args:
            config_path (str): Path to the configuration YAML file
            log_path (str): Path for logging configuration activities
        """
        # Configure logging
        self.logger = logging.getLogger('ModelConfiguration')
        self.logger.setLevel(logging.INFO)
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # File handler for logging
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        # Configuration management
        self.config_path = config_path
        self.config = self._load_configuration()

    def _load_configuration(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file with error handling.
        
        Returns:
            Dict[str, Any]: Loaded configuration dictionary
        """
        try:
            # Ensure configuration directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # Create default configuration if file doesn't exist
            if not os.path.exists(self.config_path):
                self._create_default_configuration()
            
            # Load configuration
            with open(self.config_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            return config
        
        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            # Return a minimal default configuration
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Provide a default configuration if loading fails.
        
        Returns:
            Dict[str, Any]: Default configuration dictionary
        """
        return {
            'tensorflow_model': {
                'layers': [64, 32, 16],
                'dropout_rate': 0.3,
                'learning_rate': 0.001,
                'epochs': 50,
                'batch_size': 32
            },
            'xgboost_model': {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 6,
                'early_stopping_rounds': 10
            },
            'data_preprocessing': {
                'test_size': 0.2,
                'random_state': 42
            },
            'model_paths': {
                'tensorflow_model': 'models/tensorflow_sports_predictor.h5',
                'xgboost_model': 'models/xgboost_sports_predictor.model'
            }
        }

    def _create_default_configuration(self) -> None:
        """
        Create a default configuration YAML file if it doesn't exist.
        """
        try:
            default_config = self._get_default_config()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # Write default configuration
            with open(self.config_path, 'w') as config_file:
                yaml.dump(default_config, config_file, default_flow_style=False)
            
            self.logger.info(f"Default configuration created at {self.config_path}")
        
        except Exception as e:
            self.logger.error(f"Default configuration creation failed: {e}")

    def get_model_config(
        self, 
        model_type: str = 'tensorflow'
    ) -> Dict[str, Any]:
        """
        Retrieve configuration for a specific model type.
        
        Args:
            model_type (str): Type of model ('tensorflow' or 'xgboost')
        
        Returns:
            Dict[str, Any]: Model-specific configuration
        """
        try:
            if model_type.lower() == 'tensorflow':
                return self.config.get('tensorflow_model', {})
            elif model_type.lower() == 'xgboost':
                return self.config.get('xgboost_model', {})
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        
        except Exception as e:
            self.logger.error(f"Model configuration retrieval failed: {e}")
            # Return default config for the model type
            return (
                self._get_default_config()['tensorflow_model'] 
                if model_type.lower() == 'tensorflow' 
                else self._get_default_config()['xgboost_model']
            )

    def update_configuration(
        self, 
        updates: Dict[str, Any], 
        model_type: Optional[str] = None
    ) -> None:
        """
        Update configuration with new settings.
        
        Args:
            updates (Dict[str, Any]): Configuration updates
            model_type (Optional[str]): Specific model type to update
        """
        try:
            # If no specific model type, update entire configuration
            if model_type is None:
                self.config.update(updates)
            else:
                # Update specific model configuration
                model_key = f"{model_type.lower()}_model"
                if model_key in self.config:
                    self.config[model_key].update(updates)
                else:
                    raise KeyError(f"Model type {model_type} not found in configuration")
            
            # Save updated configuration
            with open(self.config_path, 'w') as config_file:
                yaml.dump(self.config, config_file, default_flow_style=False)
            
            self.logger.info(f"Configuration updated for {model_type or 'all models'}")
        
        except Exception as e:
            self.logger.error(f"Configuration update failed: {e}")

    def get_model_path(
        self, 
        model_type: str = 'tensorflow'
    ) -> str:
        """
        Retrieve the saved model path for a specific model type.
        
        Args:
            model_type (str): Type of model ('tensorflow' or 'xgboost')
        
        Returns:
            str: Path to the saved model
        """
        try:
            model_paths = self.config.get('model_paths', {})
            
            if model_type.lower() == 'tensorflow':
                return model_paths.get(
                    'tensorflow_model', 
                    'models/tensorflow_sports_predictor.h5'
                )
            elif model_type.lower() == 'xgboost':
                return model_paths.get(
                    'xgboost_model', 
                    'models/xgboost_sports_predictor.model'
                )
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        
        except Exception as e:
            self.logger.error(f"Model path retrieval failed: {e}")
            # Return default paths
            return (
                'models/tensorflow_sports_predictor.h5' 
                if model_type.lower() == 'tensorflow' 
                else 'models/xgboost_sports_predictor.model'
            )

    def get_preprocessing_config(self) -> Dict[str, Any]:
        """
        Retrieve data preprocessing configuration.
        
        Returns:
            Dict[str, Any]: Preprocessing configuration
        """
        return self.config.get('data_preprocessing', {
            'test_size': 0.2,
            'random_state': 42
        })

def main():
    # Example usage and testing
    config_manager = ModelConfiguration()
    
    # Retrieve TensorFlow model configuration
    tf_config = config_manager.get_model_config('tensorflow')
    print("TensorFlow Model Configuration:", tf_config)
    
    # Update XGBoost model configuration
    config_manager.update_configuration(
        {'learning_rate': 0.05}, 
        model_type='xgboost'
    )

if __name__ == "__main__":
    main()