import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
import jsonschema

class DataValidator:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the DataValidator with optional logging.
        
        Args:
            logger (Optional[logging.Logger]): Logger for tracking validation processes.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def validate_dataframe_schema(self, df: pd.DataFrame, schema: Dict[str, Any]) -> bool:
        """
        Validate DataFrame against a predefined JSON schema.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            schema (Dict): JSON schema for validation
        
        Returns:
            bool: Whether the DataFrame passes schema validation
        """
        try:
            for column, column_schema in schema.get('properties', {}).items():
                if column not in df.columns:
                    if column_schema.get('required', False):
                        raise ValueError(f"Required column {column} missing")
                    continue
                
                # Type checking
                dtype = column_schema.get('type')
                if dtype == 'number':
                    if not pd.api.types.is_numeric_dtype(df[column]):
                        raise TypeError(f"Column {column} must be numeric")
                
                # Range constraints
                if dtype == 'number':
                    min_val = column_schema.get('minimum')
                    max_val = column_schema.get('maximum')
                    
                    if min_val is not None and (df[column] < min_val).any():
                        raise ValueError(f"Column {column} has values below {min_val}")
                    
                    if max_val is not None and (df[column] > max_val).any():
                        raise ValueError(f"Column {column} has values above {max_val}")
            
            return True
        
        except (ValueError, TypeError) as e:
            self.logger.error(f"Schema validation failed: {e}")
            return False
    
    def check_missing_values(self, df: pd.DataFrame, max_missing_ratio: float = 0.1) -> bool:
        """
        Check for missing values across the DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            max_missing_ratio (float): Maximum allowed ratio of missing values
        
        Returns:
            bool: Whether missing values are within acceptable limits
        """
        missing_ratios = df.isnull().mean()
        problematic_columns = missing_ratios[missing_ratios > max_missing_ratio]
        
        if not problematic_columns.empty:
            self.logger.warning("Columns with high missing value ratios:")
            for col, ratio in problematic_columns.items():
                self.logger.warning(f"{col}: {ratio * 100:.2f}% missing")
            return False
        
        return True
    
    def detect_outliers(self, df: pd.DataFrame, numeric_columns: List[str], method: str = 'iqr') -> Dict[str, List[Any]]:
        """
        Detect outliers in numeric columns using IQR or Z-score method.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            numeric_columns (List[str]): Columns to check for outliers
            method (str): Outlier detection method ('iqr' or 'zscore')
        
        Returns:
            Dict: Outliers for each column
        """
        outliers = {}
        
        for column in numeric_columns:
            if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
                continue
            
            if method == 'iqr':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                column_outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
                outliers[column] = column_outliers[column].tolist()
            
            elif method == 'zscore':
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                column_outliers = df[z_scores > 3]
                outliers[column] = column_outliers[column].tolist()
        
        return outliers
    
    def validate_data(self, 
                      df: pd.DataFrame, 
                      schema: Dict[str, Any], 
                      numeric_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Comprehensive data validation pipeline.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            schema (Dict): Validation schema
            numeric_columns (Optional[List[str]]): Columns to check for outliers
        
        Returns:
            Dict: Validation results
        """
        validation_results = {
            'schema_valid': self.validate_dataframe_schema(df, schema),
            'missing_values_valid': self.check_missing_values(df),
            'outliers': self.detect_outliers(df, numeric_columns or []) if numeric_columns else {}
        }
        
        return validation_results

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example DataFrame and configuration
    sample_data = pd.DataFrame({
        'player_score': [10.5, np.nan, 15.2, 8.7],
        'team': ['Lakers', 'Bulls', np.nan, 'Warriors'],
        'player_position': ['Guard', 'Forward', 'Center', 'Guard']
    })
    
    validation_schema = {
        'properties': {
            'player_score': {
                'type': 'number', 
                'minimum': 0, 
                'maximum': 50, 
                'required': True
            },
            'team': {
                'type': 'string'
            }
        }
    }
    
    validator = DataValidator()
    results = validator.validate_data(sample_data, validation_schema, numeric_columns=['player_score'])
    print(results)