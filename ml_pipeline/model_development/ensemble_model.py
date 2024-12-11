import logging
import numpy as np
import pandas as pd
from typing import List
from .base_model import BaseModel
from .xgboost_predictor import XGBoostPredictor
from .tensorflow_predictor import TensorFlowPredictor

class EnsembleModel(BaseModel):
    def __init__(self, model_name='ensemble_predictor', config=None):
        super().__init__(model_name, config or {})
        self.models = [
            XGBoostPredictor(config=config),
            TensorFlowPredictor(config=config)
        ]
    
    def preprocess(self, data: pd.DataFrame) -> np.ndarray:
        return data.values
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        for model in self.models:
            model.train(X_train, y_train)
        self.is_trained = all(model.is_trained for model in self.models)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            self.logger.error("Ensemble not trained")
            raise RuntimeError("Ensemble not trained")
        
        predictions = np.column_stack([model.predict(X) for model in self.models])
        return np.mean(predictions, axis=1)