import logging
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score
)
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/var/log/ml_pipeline/base_model.log'
)
logger = logging.getLogger(__name__)

class BaseMLModel(BaseEstimator, TransformerMixin, ABC):
    """
    Abstract base model for sports prop prediction models
    Provides standard interfaces and utility methods for model development
    """
    
    def __init__(
        self, 
        random_state: int = 42,
        model_config_path: str = 'config/model_config.json'
    ):
        """
        Initialize base model with configuration
        
        Args:
            random_state (int): Random seed for reproducibility
            model_config_path (str): Path to model configuration file
        """
        self.random_state = random_state
        
        # Load model configuration
        try:
            with open(model_config_path, 'r') as f:
                self.model_config = json.load(f)
            logger.info("Model configuration loaded successfully")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Model configuration loading failed: {e}")
            self.model_config = {}
    
    @abstractmethod
    def build_model(self, **kwargs):
        """
        Abstract method to build specific model architecture
        Must be implemented by child classes
        """
        pass
    
    @abstractmethod
    def train(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        **kwargs
    ):
        """
        Abstract method to train the model
        Must be implemented by child classes
        """
        pass
    
    def preprocess_data(
        self, 
        X: np.ndarray, 
        y: np.ndarray = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Basic data preprocessing method
        
        Args:
            X (np.ndarray): Input features
            y (np.ndarray, optional): Target variable
        
        Returns:
            Tuple of preprocessed X and y
        """
        # Example preprocessing steps
        # Add your standard preprocessing logic here
        X = np.nan_to_num(X)  # Replace NaN values
        
        logger.info("Basic data preprocessing completed")
        return X, y
    
    def evaluate_model(
        self, 
        X_test: np.ndarray, 
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Comprehensive model evaluation
        
        Args:
            X_test (np.ndarray): Test features
            y_test (np.ndarray): Test target
        
        Returns:
            Dictionary of performance metrics
        """
        # Predict using the trained model
        y_pred = self.predict(X_test)
        
        # Calculate regression and classification metrics
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2_score': r2_score(y_test, y_pred),
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted')
        }
        
        # Log metrics
        logger.info("Model performance metrics:")
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value}")
        
        return metrics
    
    def cross_validate(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        cv: int = 5
    ) -> Dict[str, List[float]]:
        """
        Perform cross-validation
        
        Args:
            X (np.ndarray): Input features
            y (np.ndarray): Target variable
            cv (int): Number of cross-validation folds
        
        Returns:
            Dictionary of cross-validation scores
        """
        try:
            # Validate input data
            X, y = self.preprocess_data(X, y)
            
            # Perform cross-validation
            mse_scores = cross_val_score(
                self, X, y, 
                scoring='neg_mean_squared_error', 
                cv=cv
            )
            
            r2_scores = cross_val_score(
                self, X, y, 
                scoring='r2', 
                cv=cv
            )
            
            validation_results = {
                'mse_scores': [-score for score in mse_scores],
                'r2_scores': r2_scores
            }
            
            logger.info(f"Cross-validation completed with {cv} folds")
            return validation_results
        
        except Exception as e:
            logger.error(f"Cross-validation failed: {e}")
            raise
    
    def save_model(self, output_path: str):
        """
        Save trained model to file
        
        Args:
            output_path (str): Path to save the model
        """
        import joblib
        
        try:
            joblib.dump(self, output_path)
            
            # Save model metadata
            metadata = {
                'model_type': self.__class__.__name__,
                'timestamp': datetime.now().isoformat(),
                'random_state': self.random_state
            }
            
            with open(f"{output_path}.metadata.json", 'w') as f:
                json.dump(metadata, f, indent=4)
            
            logger.info(f"Model saved to {output_path}")
        except Exception as e:
            logger.error(f"Model saving failed: {e}")
            raise
    
    @classmethod
    def load_model(cls, model_path: str):
        """
        Load a saved model
        
        Args:
            model_path (str): Path to the saved model file
        
        Returns:
            Loaded model instance
        """
        import joblib
        
        try:
            model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise