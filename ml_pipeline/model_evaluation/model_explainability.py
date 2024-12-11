import numpy as np
import pandas as pd
import shap
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
from sklearn.inspection import permutation_importance

class ModelExplainability:
    """
    Comprehensive model explainability techniques for 
    the Sports Prop Predictor project.
    """
    
    @staticmethod
    def shap_feature_importance(
        model, 
        X: np.ndarray, 
        feature_names: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate SHAP (SHapley Additive exPlanations) feature importance.
        
        Args:
            model: Trained machine learning model
            X (np.ndarray): Feature matrix
            feature_names (List[str], optional): Names of features
        
        Returns:
            Dict[str, Any]: SHAP feature importance analysis
        """
        # Use TreeExplainer for tree-based models, KernelExplainer for others
        if hasattr(model, 'predict_proba'):
            explainer = shap.TreeExplainer(model)
        else:
            explainer = shap.KernelExplainer(model.predict, X)
        
        shap_values = explainer.shap_values(X)
        
        return {
            'mean_abs_shap': np.abs(shap_values).mean(axis=0).tolist(),
            'feature_names': feature_names or [f'Feature_{i}' for i in range(X.shape[1])],
            'shap_summary_plot': shap.summary_plot(
                shap_values, 
                X, 
                feature_names=feature_names, 
                show=False
            )
        }
    
    @staticmethod
    def permutation_feature_importance(
        model, 
        X: np.ndarray, 
        y: np.ndarray, 
        feature_names: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate permutation feature importance.
        
        Args:
            model: Trained machine learning model
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target values
            feature_names (List[str], optional): Names of features
        
        Returns:
            Dict[str, Any]: Permutation feature importance
        """
        perm_importance = permutation_importance(
            model, 
            X, 
            y, 
            n_repeats=10, 
            random_state=42
        )
        
        return {
            'importance_mean': perm_importance.importances_mean.tolist(),
            'importance_std': perm_importance.importances_std.tolist(),
            'feature_names': feature_names or [f'Feature_{i}' for i in range(X.shape[1])]
        }
    
    @classmethod
    def model_explanation_report(
        cls,
        model,
        X: np.ndarray, 
        y: np.ndarray,
        feature_names: List[str] = None,
        report_path: str = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive model explanation report.
        
        Args:
            model: Trained machine learning model
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target values
            feature_names (List[str], optional): Names of features
            report_path (str, optional): Path to save the report
        
        Returns:
            Dict[str, Any]: Comprehensive model explanation report
        """
        report = {
            'shap_importance': cls.shap_feature_importance(
                model, X, feature_names
            ),
            'permutation_importance': cls.permutation_feature_importance(
                model, X, y, feature_names
            )
        }
        
        if report_path:
            cls._save_report(report, report_path)
        
        return report
    
    @staticmethod
    def _save_report(report: Dict[str, Any], path: str) -> None:
        """
        Save model explanation report to a file.
        
        Args:
            report (Dict[str, Any]): Model explanation report dictionary
            path (str): File path to save the report
        """
        with open(path, 'w') as f:
            import json
            json.dump(report, f, indent=4)
    
    @staticmethod
    def generate_feature_importance_plot(
        importances: List[float], 
        feature_names: List[str], 
        title: str = 'Feature Importance'
    ) -> go.Figure:
        """
        Generate an interactive feature importance plot.
        
        Args:
            importances (List[float]): Feature importance scores
            feature_names (List[str]): Names of features
            title (str, optional): Plot title
        
        Returns:
            go.Figure: Interactive feature importance plot
        """
        # Sort features by importance in descending order
        sorted_indices = np.argsort(importances)[::-1]
        sorted_importances = [importances[i] for i in sorted_indices]
        sorted_features = [feature_names[i] for i in sorted_indices]
        
        fig = go.Figure(
            data=[go.Bar(
                x=sorted_importances, 
                y=sorted_features, 
                orientation='h',
                marker_color='rgba(50, 171, 96, 0.6)',
                text=sorted_importances,
                textposition='auto'
            )]
        )
        
        fig.update_layout(
            title=title,
            xaxis_title='Feature Importance',
            yaxis_title='Features',
            height=600,
            width=800,
            margin=dict(l=200, r=50, t=50, b=50)
        )
        
        return fig
    
    @staticmethod
    def partial_dependence_plot(
        model, 
        X: np.ndarray, 
        feature_index: int, 
        feature_name: str = None
    ) -> go.Figure:
        """
        Generate a partial dependence plot for a specific feature.
        
        Args:
            model: Trained machine learning model
            X (np.ndarray): Feature matrix
            feature_index (int): Index of the feature to analyze
            feature_name (str, optional): Name of the feature
        
        Returns:
            go.Figure: Partial dependence plot
        """
        from sklearn.inspection import partial_dependence
        
        # Create a copy of X to avoid modifying the original
        X_copy = X.copy()
        
        # Generate partial dependence
        pd_results = partial_dependence(
            model, 
            X_copy, 
            features=[feature_index], 
            grid_resolution=100
        )
        
        # Extract values
        feature_values = pd_results['values'][0]
        pd_values = pd_results['average'][0]
        
        # Create plot
        fig = go.Figure(
            data=[go.Scatter(
                x=feature_values, 
                y=pd_values, 
                mode='lines+markers',
                name='Partial Dependence'
            )]
        )
        
        fig.update_layout(
            title=f'Partial Dependence Plot for {feature_name or f"Feature {feature_index}"}',
            xaxis_title=feature_name or f'Feature {feature_index}',
            yaxis_title='Partial Dependence',
            height=400,
            width=600
        )
        
        return fig