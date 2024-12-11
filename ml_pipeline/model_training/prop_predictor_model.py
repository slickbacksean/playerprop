import os
import logging
import numpy as np
import pandas as pd
import xgboost as xgb
import tensorflow as tf
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score
)

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('prop_predictor_model_training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PropPredictorModel:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the PropPredictor Model with configuration settings.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary for model parameters
        """
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        
        # Set random seeds for reproducibility
        np.random.seed(self.config.get('random_seed', 42))
        tf.random.set_seed(self.config.get('random_seed', 42))
        
        logger.info(f"PropPredictorModel initialized with config: {config}")
    
    def load_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and preprocess training data.
        
        Args:
            data_path (str): Path to the training data CSV
        
        Returns:
            Tuple of X (features) and y (target) data
        """
        try:
            logger.info(f"Loading data from {data_path}")
            df = pd.read_csv(data_path)
            
            # Validate data
            if df.empty:
                raise ValueError("Loaded dataset is empty")
            
            # Separate features and target
            features = self.config.get('features', [])
            target = self.config.get('target', 'prop_result')
            
            X = df[features]
            y = df[target]
            
            logger.info(f"Data loaded successfully. Shape: {X.shape}")
            return X, y
        
        except FileNotFoundError:
            logger.error(f"Data file not found at {data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess data by scaling features and splitting into train/test sets.
        
        Args:
            X (pd.DataFrame): Feature data
            y (pd.Series): Target data
        
        Returns:
            Tuple of train and test datasets
        """
        try:
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, 
                y, 
                test_size=self.config.get('test_size', 0.2),
                random_state=self.config.get('random_seed', 42)
            )
            
            logger.info(f"Data preprocessed. Train shape: {X_train.shape}, Test shape: {X_test.shape}")
            return X_train, X_test, y_train, y_test
        
        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise
    
    def train_xgboost_model(self, X_train: np.ndarray, y_train: np.ndarray) -> xgb.XGBRegressor:
        """
        Train an XGBoost regression model.
        
        Args:
            X_train (np.ndarray): Scaled training features
            y_train (np.ndarray): Training target values
        
        Returns:
            Trained XGBoost model
        """
        try:
            # XGBoost hyperparameters from config
            xgb_params = self.config.get('xgboost_params', {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 5,
                'objective': 'reg:squarederror'
            })
            
            logger.info("Training XGBoost model")
            model = xgb.XGBRegressor(**xgb_params)
            model.fit(X_train, y_train)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
            logger.info(f"Cross-validation MSE scores: {-cv_scores}")
            logger.info(f"Mean CV Score: {-cv_scores.mean()}")
            
            return model
        
        except Exception as e:
            logger.error(f"Error training XGBoost model: {e}")
            raise
    
    def evaluate_model(self, model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance using multiple metrics.
        
        Args:
            model: Trained machine learning model
            X_test (np.ndarray): Scaled test features
            y_test (np.ndarray): Test target values
        
        Returns:
            Dictionary of performance metrics
        """
        try:
            # Predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2_score': r2_score(y_test, y_pred)
            }
            
            # Log metrics
            for metric, value in metrics.items():
                logger.info(f"{metric.upper()}: {value}")
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            raise
    
    def save_model(self, model, metrics: Dict[str, float]):
        """
        Save trained model and performance metrics.
        
        Args:
            model: Trained machine learning model
            metrics (Dict[str, float]): Model performance metrics
        """
        try:
            # Create model directory if it doesn't exist
            os.makedirs('models', exist_ok=True)
            
            # Timestamp for model versioning
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save model
            model_path = f"models/prop_predictor_{timestamp}.model"
            model.save_model(model_path)
            
            # Save metrics
            import json
            with open(f"models/metrics_{timestamp}.json", 'w') as f:
                json.dump(metrics, f)
            
            logger.info(f"Model saved to {model_path}")
            logger.info(f"Metrics saved to models/metrics_{timestamp}.json")
        
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def run_training_pipeline(self, data_path: str):
        """
        Execute complete model training pipeline.
        
        Args:
            data_path (str): Path to training data
        """
        try:
            logger.info("Starting PropPredictor Model Training Pipeline")
            
            # Load data
            X, y = self.load_data(data_path)
            
            # Preprocess data
            X_train, X_test, y_train, y_test = self.preprocess_data(X, y)
            
            # Train model
            model = self.train_xgboost_model(X_train, y_train)
            
            # Evaluate model
            metrics = self.evaluate_model(model, X_test, y_test)
            
            # Save model
            self.save_model(model, metrics)
            
            logger.info("PropPredictor Model Training Pipeline Completed Successfully")
        
        except Exception as e:
            logger.error(f"Model training pipeline failed: {e}")
            raise

def main():
    # Example configuration
    config = {
        'random_seed': 42,
        'test_size': 0.2,
        'features': [
            'player_stats', 'team_performance', 
            'historical_odds', 'recent_form'
        ],
        'target': 'prop_result',
        'xgboost_params': {
            'n_estimators': 200,
            'learning_rate': 0.05,
            'max_depth': 6
        }
    }
    
    try:
        # Instantiate and run model training
        prop_predictor = PropPredictorModel(config)
        prop_predictor.run_training_pipeline('data/sports_prop_data.csv')
    
    except Exception as e:
        logger.error(f"Training script execution failed: {e}")

if __name__ == "__main__":
    main()