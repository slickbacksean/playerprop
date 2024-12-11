import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List
from sklearn.model_selection import (
    KFold, 
    StratifiedKFold, 
    TimeSeriesSplit, 
    cross_val_score, 
    cross_validate
)
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score, 
    mean_absolute_percentage_error
)

class CrossValidator:
    """
    Advanced cross-validation module for sports prediction models
    Supports multiple cross-validation strategies and detailed performance tracking
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize cross-validator with configuration
        
        Args:
            config (Dict[str, Any]): Configuration for cross-validation
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Cross-validation strategies
        self.cv_strategies = {
            'kfold': KFold,
            'stratified_kfold': StratifiedKFold,
            'time_series': TimeSeriesSplit
        }
        
        # Performance metrics
        self.metrics = {
            'mse': mean_squared_error,
            'mae': mean_absolute_error,
            'r2': r2_score,
            'mape': mean_absolute_percentage_error
        }
    
    def _select_cv_strategy(self, strategy: str = 'kfold', **kwargs) -> Any:
        """
        Select appropriate cross-validation strategy
        
        Args:
            strategy (str): Cross-validation strategy name
            **kwargs: Additional parameters for CV strategy
        
        Returns:
            Cross-validation strategy object
        """
        try:
            cv_class = self.cv_strategies.get(strategy.lower())
            if not cv_class:
                raise ValueError(f"Unsupported CV strategy: {strategy}")
            
            # Default parameters with override
            default_params = {
                'n_splits': self.config.get('cv_splits', 5),
                'shuffle': True,
                'random_state': 42
            }
            default_params.update(kwargs)
            
            return cv_class(**default_params)
        
        except Exception as e:
            self.logger.error(f"Error selecting CV strategy: {e}")
            raise
    
    def validate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Perform cross-validation with comprehensive performance tracking
        
        Args:
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target vector
        
        Returns:
            Dict of cross-validation results
        """
        try:
            # Select CV strategy based on configuration
            cv_strategy = self._select_cv_strategy(
                self.config.get('cv_strategy', 'kfold')
            )
            
            # Detailed cross-validation
            cv_results = cross_validate(
                estimator=self.config.get('model'),
                X=X,
                y=y,
                cv=cv_strategy,
                scoring=list(self.metrics.keys()),
                return_train_score=True
            )
            
            # Compute detailed performance summary
            performance_summary = {
                metric: {
                    'test_mean': np.mean(cv_results[f'test_{metric}']),
                    'test_std': np.std(cv_results[f'test_{metric}']),
                    'train_mean': np.mean(cv_results[f'train_{metric}']),
                    'train_std': np.std(cv_results[f'train_{metric}'])
                }
                for metric in self.metrics.keys()
            }
            
            # Log performance
            self.logger.info("Cross-validation completed successfully")
            for metric, stats in performance_summary.items():
                self.logger.info(f"{metric.upper()} Performance: {stats}")
            
            return {
                'cv_strategy': str(cv_strategy),
                'performance_summary': performance_summary,
                'raw_results': cv_results
            }
        
        except Exception as e:
            self.logger.error(f"Cross-validation failed: {e}")
            raise
    
    def variance_analysis(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Analyze variance and potential overfitting
        
        Args:
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target vector
        
        Returns:
            Dict of variance metrics
        """
        try:
            train_scores, test_scores = [], []
            
            # Iterative variance analysis
            for train_idx, test_idx in self._select_cv_strategy().split(X):
                X_train, X_test = X[train_idx], X[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                
                model = self.config.get('model')
                model.fit(X_train, y_train)
                
                train_scores.append(model.score(X_train, y_train))
                test_scores.append(model.score(X_test, y_test))
            
            variance_report = {
                'train_variance': np.var(train_scores),
                'test_variance': np.var(test_scores),
                'performance_gap': np.mean(train_scores) - np.mean(test_scores)
            }
            
            self.logger.info("Variance Analysis Complete")
            self.logger.info(f"Variance Report: {variance_report}")
            
            return variance_report
        
        except Exception as e:
            self.logger.error(f"Variance analysis failed: {e}")
            raise