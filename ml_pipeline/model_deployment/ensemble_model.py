import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.ensemble import VotingRegressor, StackingRegressor
from sklearn.model_selection import train_test_split
from .base_model import BaseMLModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/var/log/ml_pipeline/ensemble_model.log'
)
logger = logging.getLogger(__name__)

class EnsemblePredictor(BaseMLModel):
    """
    Ensemble model combining multiple predictors for sports prop predictions
    Supports voting and stacking ensemble methods
    """
    
    def __init__(
        self, 
        base_models: List[BaseMLModel] = None,
        ensemble_type: str = 'stacking',
        random_state: int = 42
    ):
        """
        Initialize ensemble model
        
        Args:
            base_models (List[BaseMLModel]): List of base models to ensemble
            ensemble_type (str): Type of ensemble ('voting' or 'stacking')
            random_state (int): Random seed for reproducibility
        """
        super().__init__(random_state=random_state)
        
        self.base_models = base_models or []
        self.ensemble_type = ensemble_type
        self.ensemble_model = None
    
    def build_model(
        self, 
        base_models: List[BaseMLModel] = None,
        weights: List[float] = None
    ):
        """
        Build ensemble model
        
        Args:
            base_models (List[BaseMLModel], optional): Base models to use
            weights (List[float], optional): Weights for each model in ensemble
        """
        # Use provided base models or existing base models
        models_to_use = base_models or self.base_models
        
        if not models_to_use:
            raise ValueError("No base models provided for ensemble")
        
        try:
            if self.ensemble_type == 'voting':
                self.ensemble_model = VotingRegressor(
                    estimators=[(str(i), model) for i, model in enumerate(models_to_use)],
                    weights=weights
                )
            
            elif self.ensemble_type == 'stacking':
                self.ensemble_model = StackingRegressor(
                    estimators=[(str(i), model) for i, model in enumerate(models_to_use)],
                    final_estimator=models_to_use[-1]  # Last model as final estimator
                )
            
            else:
                raise ValueError(f"Unsupported ensemble type: {self.ensemble_type}")
            
            logger.info(f"Ensemble model built with {len(models_to_use)} base models")
        
        except Exception as e:
            logger.error(f"Ensemble model building failed: {e}")
            raise
    
    def train(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        test_size: float = 0.2
    ):
        """
        Train ensemble model
        
        Args:
            X (np.ndarray): Input features
            y (np.ndarray): Target variable
            test_size (float): Proportion of data for testing
        """
        # Preprocess data
        X, y = self.preprocess_data(X, y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=self.random_state
        )
        
        try:
            # Build ensemble if not already built
            if self.ensemble_model is None:
                self.build_model()
            
            # Train base models first
            for model in self.base_models:
                model.train(X_train, y_train)
            
            # Train ensemble model
            self.ensemble_model.fit(X_train, y_train)
            
            # Evaluate model
            performance = self.evaluate_model(X_test, y_test)
            logger.info("Ensemble model training completed")
            
            return performance
        
        except Exception as e:
            logger.error(f"Ensemble model training failed: {e}")
            raise
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generate predictions using ensemble model
        
        Args:
            X (np.ndarray): Input features
        
        Returns:
            np.ndarray: Predictions
        """
        if self.ensemble_model is None:
            raise ValueError("Ensemble model not trained")
        
        try:
            X, _ = self.preprocess_data(X)
            predictions = self.ensemble_model.predict(X)
            logger.info("Ensemble predictions generated")
            return predictions
        
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {e}")
            raise
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Generate prediction probabilities
        
        Args:
            X (np.ndarray): Input features
        
        Returns:
            np.ndarray: Prediction probabilities
        """
        # Probabilistic prediction might require individual base model support
        try:
            X, _ = self.preprocess_data(X)
            probas = [
                model.predict_proba(X) 
                for model in self.base_models 
                if hasattr(model, 'predict_proba')
            ]
            
            # Average probabilities
            if probas:
                return np.mean(probas, axis=0)
            
            logger.warning("Probabilistic prediction not supported by base models")
            return None
        
        except Exception as e:
            logger.error(f"Probabilistic prediction failed: {e}")
            raise