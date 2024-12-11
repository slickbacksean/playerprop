import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.preprocessing import LabelEncoder
from fairlearn.metrics import (
    demographic_parity_difference,
    equalized_odds_difference,
    disparate_impact
)

class BiasDetector:
    """
    Comprehensive bias detection and mitigation for machine learning models
    in the Sports Prop Predictor project.
    """
    
    @staticmethod
    def detect_demographic_bias(
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        sensitive_features: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Detect bias across different demographic groups.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            sensitive_features (pd.DataFrame): DataFrame with sensitive attribute columns
        
        Returns:
            Dict[str, float]: Bias metrics for each sensitive attribute
        """
        bias_results = {}
        
        for column in sensitive_features.columns:
            # Convert sensitive feature to numeric if categorical
            if sensitive_features[column].dtype == 'object':
                le = LabelEncoder()
                feature_numeric = le.fit_transform(sensitive_features[column])
            else:
                feature_numeric = sensitive_features[column]
            
            bias_results[column] = {
                'demographic_parity_diff': demographic_parity_difference(
                    y_true, y_pred, sensitive_features=feature_numeric
                ),
                'equalized_odds_diff': equalized_odds_difference(
                    y_true, y_pred, sensitive_features=feature_numeric
                ),
                'disparate_impact': disparate_impact(
                    y_true, y_pred, sensitive_features=feature_numeric
                )
            }
        
        return bias_results
    
    @staticmethod
    def detect_prediction_bias(
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        sensitive_features: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        """
        Detect prediction biases across different groups.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            sensitive_features (pd.DataFrame): DataFrame with sensitive attribute columns
        
        Returns:
            Dict[str, Dict[str, float]]: Detailed prediction bias metrics
        """
        from sklearn.metrics import precision_score, recall_score
        
        bias_analysis = {}
        
        for column in sensitive_features.columns:
            unique_groups = sensitive_features[column].unique()
            
            group_metrics = {}
            for group in unique_groups:
                group_mask = sensitive_features[column] == group
                
                group_metrics[str(group)] = {
                    'precision': precision_score(
                        y_true[group_mask], 
                        y_pred[group_mask], 
                        zero_division=0
                    ),
                    'recall': recall_score(
                        y_true[group_mask], 
                        y_pred[group_mask], 
                        zero_division=0
                    ),
                    'group_representation': group_mask.sum() / len(group_mask)
                }
            
            bias_analysis[column] = group_metrics
        
        return bias_analysis
    
    @classmethod
    def generate_bias_report(
        cls, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        sensitive_features: pd.DataFrame,
        report_path: str = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive bias detection report.
        
        Args:
            y_true (np.ndarray): True target values
            y_pred (np.ndarray): Predicted target values
            sensitive_features (pd.DataFrame): DataFrame with sensitive attribute columns
            report_path (str, optional): Path to save the report
        
        Returns:
            Dict[str, Any]: Comprehensive bias detection report
        """
        report = {
            'demographic_bias': cls.detect_demographic_bias(y_true, y_pred, sensitive_features),
            'prediction_bias': cls.detect_prediction_bias(y_true, y_pred, sensitive_features)
        }
        
        if report_path:
            cls._save_report(report, report_path)
        
        return report
    
    @staticmethod
    def _save_report(report: Dict[str, Any], path: str) -> None:
        """
        Save bias detection report to a file.
        
        Args:
            report (Dict[str, Any]): Bias detection report dictionary
            path (str): File path to save the report
        """
        with open(path, 'w') as f:
            import json
            json.dump(report, f, indent=4)