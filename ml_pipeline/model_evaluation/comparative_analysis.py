import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import Dict, List, Any, Callable
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score
)

class ComparativeModelAnalysis:
    """
    Comprehensive model comparison and analysis for 
    the Sports Prop Predictor project.
    """
    
    @staticmethod
    def cross_validation_comparison(
        models: Dict[str, Any], 
        X: np.ndarray, 
        y: np.ndarray, 
        cv: int = 5
    ) -> Dict[str, Dict[str, float]]:
        """
        Perform cross-validation comparison across multiple models.
        
        Args:
            models (Dict[str, Any]): Dictionary of models to compare
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target values
            cv (int, optional): Number of cross-validation folds
        
        Returns:
            Dict[str, Dict[str, float]]: Cross-validation performance metrics
        """
        cv_results = {}
        
        for name, model in models.items():
            # Perform cross-validation
            mse_scores = cross_val_score(
                model, 
                X, 
                y, 
                cv=cv, 
                scoring='neg_mean_squared_error'
            )
            
            r2_scores = cross_val_score(
                model, 
                X, 
                y, 
                cv=cv, 
                scoring='r2'
            )
            
            cv_results[name] = {
                'mean_cv_mse': -mse_scores.mean(),
                'std_cv_mse': mse_scores.std(),
                'mean_cv_r2': r2_scores.mean(),
                'std_cv_r2': r2_scores.std()
            }
        
        return cv_results
    
    @staticmethod
    def performance_comparison(
        models: Dict[str, Any], 
        X_train: np.ndarray, 
        X_test: np.ndarray, 
        y_train: np.ndarray, 
        y_test: np.ndarray
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare model performance on test data.
        
        Args:
            models (Dict[str, Any]): Dictionary of models to compare
            X_train (np.ndarray): Training feature matrix
            X_test (np.ndarray): Testing feature matrix
            y_train (np.ndarray): Training target values
            y_test (np.ndarray): Testing target values
        
        Returns:
            Dict[str, Dict[str, float]]: Performance metrics for each model
        """
        performance_results = {}
        
        for name, model in models.items():
            # Train the model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            performance_results[name] = {
                'mean_squared_error': mean_squared_error(y_test, y_pred),
                'mean_absolute_error': mean_absolute_error(y_test, y_pred),
                'r2_score': r2_score(y_test, y_pred)
            }
        
        return performance_results
    
    @staticmethod
    def generate_performance_comparison_plot(
        performance_results: Dict[str, Dict[str, float]]
    ) -> go.Figure:
        """
        Generate an interactive bar plot comparing model performances.
        
        Args:
            performance_results (Dict[str, Dict[str, float]]): Performance metrics
        
        Returns:
            go.Figure: Interactive comparison plot
        """
        # Prepare data for plotting
        models = list(performance_results.keys())
        mse_values = [results['mean_squared_error'] for results in performance_results.values()]
        mae_values = [results['mean_absolute_error'] for results in performance_results.values()]
        r2_values = [results['r2_score'] for results in performance_results.values()]
        
        # Create subplot figure
        fig = go.Figure()
        
        # MSE Bars
        fig.add_trace(go.Bar(
            x=models,
            y=mse_values,
            name='Mean Squared Error',
            marker_color='blue'
        ))
        
        # MAE Bars
        fig.add_trace(go.Bar(
            x=models,
            y=mae_values,
            name='Mean Absolute Error',
            marker_color='green'
        ))
        
        # R2 Line
        fig.add_trace(go.Scatter(
            x=models,
            y=r2_values,
            name='R2 Score',
            mode='lines+markers',
            marker_color='red',
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            title='Model Performance Comparison',
            xaxis_title='Models',
            yaxis_title='Error Metrics',
            yaxis2=dict(
                title='R2 Score',
                overlaying='y',
                side='right'
            ),
            barmode='group',
            height=600,
            width=800
        )
        
        return fig
    
    @classmethod
    def comprehensive_model_comparison(
        cls,
        models: Dict[str, Any], 
        X: np.ndarray, 
        y: np.ndarray, 
        test_size: float = 0.2,
        random_state: int = 42,
        report_path: str = None
    ) -> Dict[str, Any]:
        """
        Perform a comprehensive comparison of multiple models.
        
        Args:
            models (Dict[str, Any]): Dictionary of models to compare
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target values
            test_size (float, optional): Proportion of test set
            random_state (int, optional): Random seed for reproducibility
            report_path (str, optional): Path to save the report
        
        Returns:
            Dict[str, Any]: Comprehensive model comparison report
        """
        from sklearn.model_selection import train_test_split
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state
        )
        
        # Perform cross-validation comparison
        cv_results = cls.cross_validation_comparison(models, X, y)
        
        # Perform performance comparison on test set
        performance_results = cls.performance_comparison(
            models, X_train, X_test, y_train, y_test
        )
        
        # Generate comparison report
        report = {
            'cross_validation_results': cv_results,
            'test_performance_results': performance_results
        }
        
        # Generate and save performance plot
        performance_plot = cls.generate_performance_comparison_plot(performance_results)
        performance_plot.write_html(report_path + '_performance_plot.html') if report_path else None
        
        # Save report if path provided
        if report_path:
            import json
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=4)
        
        return report