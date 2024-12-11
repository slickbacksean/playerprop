import logging
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transfer_learning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TransferLearningPredictor:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize transfer learning model with configuration.
        
        Args:
            config (Dict[str, Any]): Configuration parameters for transfer learning
        """
        self.config = config
        self.base_model = None
        self.transfer_model = None
        self.scaler = StandardScaler()
        
        # Set random seeds for reproducibility
        np.random.seed(self.config.get('random_seed', 42))
        tf.random.set_seed(self.config.get('random_seed', 42))
        
        logger.info(f"Transfer Learning Predictor initialized with config: {config}")
    
    def load_pretrained_model(self, model_path: str) -> tf.keras.Model:
        """
        Load a pre-trained base model for transfer learning.
        
        Args:
            model_path (str): Path to the pre-trained model
        
        Returns:
            Loaded base model
        """
        try:
            logger.info(f"Loading pre-trained model from {model_path}")
            
            # Check if model exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Pre-trained model not found at {model_path}")
            
            # Load model with custom objects if needed
            base_model = tf.keras.models.load_model(
                model_path, 
                custom_objects=self.config.get('custom_objects', {})
            )
            
            # Freeze base model layers
            for layer in base_model.layers:
                layer.trainable = False
            
            logger.info("Pre-trained model loaded and base layers frozen")
            return base_model
        
        except Exception as e:
            logger.error(f"Error loading pre-trained model: {e}")
            raise
    
    def prepare_transfer_learning_model(
        self, 
        base_model: tf.keras.Model, 
        input_shape: Tuple[int, ...], 
        num_classes: int
    ) -> tf.keras.Model:
        """
        Prepare transfer learning model by adding custom layers.
        
        Args:
            base_model (tf.keras.Model): Pre-trained base model
            input_shape (Tuple[int, ...]): Input data shape
            num_classes (int): Number of output classes
        
        Returns:
            Transfer learning model
        """
        try:
            logger.info("Preparing transfer learning model architecture")
            
            # Create transfer learning model
            transfer_model = tf.keras.Sequential([
                base_model,
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(
                    self.config.get('dense_units', 128), 
                    activation='relu'
                ),
                tf.keras.layers.Dropout(
                    self.config.get('dropout_rate', 0.5)
                ),
                tf.keras.layers.Dense(
                    num_classes, 
                    activation='softmax'
                )
            ])
            
            # Compile model with configured optimizer and loss
            transfer_model.compile(
                optimizer=tf.keras.optimizers.Adam(
                    learning_rate=self.config.get('learning_rate', 0.0001)
                ),
                loss=self.config.get('loss_function', 'categorical_crossentropy'),
                metrics=['accuracy']
            )
            
            logger.info("Transfer learning model prepared successfully")
            return transfer_model
        
        except Exception as e:
            logger.error(f"Error preparing transfer learning model: {e}")
            raise
    
    def load_and_preprocess_data(
        self, 
        data_path: str, 
        features: List[str], 
        target: str
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Load and preprocess data for transfer learning.
        
        Args:
            data_path (str): Path to training data
            features (List[str]): List of feature columns
            target (str): Target column name
        
        Returns:
            Preprocessed train and test datasets
        """
        try:
            logger.info(f"Loading data from {data_path}")
            
            # Load data
            df = pd.read_csv(data_path)
            
            # Validate data
            if df.empty:
                raise ValueError("Loaded dataset is empty")
            
            X = df[features]
            y = pd.get_dummies(df[target])  # One-hot encode target
            
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
            logger.error(f"Error loading and preprocessing data: {e}")
            raise
    
    def train_transfer_model(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_test: np.ndarray, 
        y_test: np.ndarray
    ) -> tf.keras.Model:
        """
        Train transfer learning model.
        
        Args:
            X_train, y_train: Training data
            X_test, y_test: Test data
        
        Returns:
            Trained transfer learning model
        """
        try:
            logger.info("Starting transfer learning model training")
            
            # Early stopping and model checkpointing
            early_stopping = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', 
                patience=5, 
                restore_best_weights=True
            )
            
            model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
                'best_transfer_model.h5', 
                save_best_only=True
            )
            
            # Train model
            history = self.transfer_model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=self.config.get('epochs', 50),
                batch_size=self.config.get('batch_size', 32),
                callbacks=[early_stopping, model_checkpoint],
                verbose=1
            )
            
            # Evaluate model
            test_loss, test_accuracy = self.transfer_model.evaluate(X_test, y_test)
            logger.info(f"Test Loss: {test_loss}, Test Accuracy: {test_accuracy}")
            
            return self.transfer_model
        
        except Exception as e:
            logger.error(f"Error during transfer learning training: {e}")
            raise
    
    def run_transfer_learning_pipeline(
        self, 
        pretrained_model_path: str, 
        data_path: str, 
        features: List[str], 
        target: str
    ):
        """
        Execute complete transfer learning pipeline.
        
        Args:
            pretrained_model_path (str): Path to pre-trained model
            data_path (str): Path to training data
            features (List[str]): Feature columns
            target (str): Target column
        """
        try:
            logger.info("Starting Transfer Learning Pipeline")
            
            # Load pre-trained base model
            self.base_model = self.load_pretrained_model(pretrained_model_path)
            
            # Load and preprocess data
            X_train, X_test, y_train, y_test = self.load_and_preprocess_data(
                data_path, features, target
            )
            
            # Prepare transfer learning model
            self.transfer_model = self.prepare_transfer_learning_model(
                self.base_model, 
                input_shape=X_train.shape[1:], 
                num_classes=y_train.shape[1]
            )
            
            # Train transfer model
            trained_model = self.train_transfer_model(
                X_train, y_train, X_test, y_test
            )
            
            logger.info("Transfer Learning Pipeline Completed Successfully")
            return trained_model
        
        except Exception as e:
            logger.error(f"Transfer learning pipeline failed: {e}")
            raise

def main():
    # Example configuration
    config = {
        'random_seed': 42,
        'test_size': 0.2,
        'learning_rate': 0.0001,
        'epochs': 50,
        'batch_size': 32,
        'dense_units': 128,
        'dropout_rate': 0.5,
        'loss_function': 'categorical_crossentropy'
    }
    
    try:
        # Instantiate transfer learning predictor
        transfer_learner = TransferLearningPredictor(config)
        
        # Run transfer learning pipeline
        transfer_learner.run_transfer_learning_pipeline(
            pretrained_model_path='models/base_sports_model.h5',
            data_path='data/sports_prop_transfer_data.csv',
            features=['player_stats', 'team_performance'],
            target='prop_category'
        )
    
    except Exception as e:
        logger.error(f"Transfer learning script execution failed: {e}")

if __name__ == "__main__":
    main()