import numpy as np
import pandas as pd
from typing import Dict, List, Any
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix
)

class PerformanceMetrics:
    """
    Comprehensive performance metrics calculation for machine learning models
    in the Sports Prop Predictor project.
    """
    
    @staticmethod
    def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate regression performance metrics.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
        
        Returns:
            Dict[str, float]: Dictionary of performance metrics
        """
        return {
            'mean_squared_error': mean_squared_error(y_true, y_pred),
            'root_mean_squared_error': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mean_absolute_error': mean_absolute_error(y_true, y_pred),
            'r2_score': r2_score(y_true, y_pred)
        }
    
    @staticmethod
    def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, avg: str = 'weighted') -> Dict[str, float]:
        """
        Calculate classification performance metrics.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            avg (str, optional): Averaging method for multi-class metrics. Defaults to 'weighted'.
        
        Returns:
            Dict[str, float]: Dictionary of performance metrics
        """
        return {
            'precision': precision_score(y_true, y_pred, average=avg),
            'recall': recall_score(y_true, y_pred, average=avg),
            'f1_score': f1_score(y_true, y_pred, average=avg),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
    
    @staticmethod
    def time_series_metrics(
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        prediction_horizon: int = 1
    ) -> Dict[str, float]:
        """
        Calculate time series specific performance metrics.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            prediction_horizon (int): Number of time steps predicted ahead
        
        Returns:
            Dict[str, float]: Dictionary of time series performance metrics
        """
        # Shift series to account for prediction horizon
        y_true_shifted = y_true[prediction_horizon:]
        y_pred_shifted = y_pred[:-prediction_horizon]
        
        return {
            'horizon_mae': mean_absolute_error(y_true_shifted, y_pred_shifted),
            'horizon_rmse': np.sqrt(mean_squared_error(y_true_shifted, y_pred_shifted)),
            'prediction_horizon': prediction_horizon
        }
    
    @classmethod
    def generate_performance_report(
        cls, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        model_name: str = 'Unnamed Model',
        report_path: str = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            model_name (str, optional): Name of the model being evaluated
            report_path (str, optional): Path to save the report
        
        Returns:
            Dict[str, Any]: Comprehensive performance report
        """
        report = {
            'model_name': model_name,
            'regression_metrics': cls.regression_metrics(y_true, y_pred),
            'classification_metrics': cls.classification_metrics(y_true, y_pred),
            'time_series_metrics': cls.time_series_metrics(y_true, y_pred)
        }
        
        if report_path:
            cls._save_report(report, report_path)
        
        return report
    
    @staticmethod
    def _save_report(report: Dict[str, Any], path: str) -> None:
        """
        Save performance report to a file.
        
        Args:
            report (Dict[str, Any]): Performance report dictionary
            path (str): File path to save the report
        """
        with open(path, 'w') as f:
            import json
            json.dump(report, f, indent=4)