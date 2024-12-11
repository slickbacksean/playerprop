import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

class DataCleaner:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the DataCleaner with optional logging.
        
        Args:
            logger (Optional[logging.Logger]): Logger for tracking cleaning processes.
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def clean_numeric_columns(self, df: pd.DataFrame, numeric_columns: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Clean and standardize numeric columns with configurable handling.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            numeric_columns (Dict): Configuration for numeric column cleaning
        
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        for column, config in numeric_columns.items():
            if column not in df.columns:
                self.logger.warning(f"Column {column} not found in DataFrame")
                continue
            
            # Handle missing values
            if config.get('fill_method', 'zero') == 'zero':
                df[column] = df[column].fillna(0)
            elif config.get('fill_method') == 'median':
                df[column] = df[column].fillna(df[column].median())
            
            # Apply range constraints
            if 'min_value' in config:
                df[column] = df[column].clip(lower=config['min_value'])
            if 'max_value' in config:
                df[column] = df[column].clip(upper=config['max_value'])
            
            # Data type conversion
            if config.get('convert_to'):
                df[column] = df[column].astype(config['convert_to'])
        
        return df
    
    def clean_categorical_columns(self, df: pd.DataFrame, categorical_columns: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Clean and standardize categorical columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            categorical_columns (Dict): Configuration for categorical column cleaning
        
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        for column, config in categorical_columns.items():
            if column not in df.columns:
                self.logger.warning(f"Column {column} not found in DataFrame")
                continue
            
            # Handle missing values
            if config.get('fill_method') == 'mode':
                df[column] = df[column].fillna(df[column].mode()[0])
            elif config.get('fill_method') == 'unknown':
                df[column] = df[column].fillna('Unknown')
            
            # Standardize case
            if config.get('lowercase', False):
                df[column] = df[column].str.lower()
            
            # Replace values
            if config.get('replacements'):
                df[column] = df[column].replace(config['replacements'])
        
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[list] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            subset (Optional[list]): Columns to consider for duplicate detection
        
        Returns:
            pd.DataFrame: DataFrame with duplicates removed
        """
        initial_rows = len(df)
        df = df.drop_duplicates(subset=subset)
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            self.logger.info(f"Removed {removed_rows} duplicate rows")
        
        return df
    
    def clean_data(self, 
                   df: pd.DataFrame, 
                   numeric_columns: Dict[str, Dict[str, Any]], 
                   categorical_columns: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
        """
        Comprehensive data cleaning pipeline.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            numeric_columns (Dict): Configuration for numeric columns
            categorical_columns (Dict): Configuration for categorical columns
        
        Returns:
            pd.DataFrame: Fully cleaned DataFrame
        """
        df = self.remove_duplicates(df)
        df = self.clean_numeric_columns(df, numeric_columns)
        df = self.clean_categorical_columns(df, categorical_columns)
        
        return df

# Example usage and configuration
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example DataFrame and configuration
    sample_data = pd.DataFrame({
        'player_score': [10.5, np.nan, 15.2, 8.7],
        'team': ['Lakers', 'Bulls', np.nan, 'Warriors'],
        'player_position': ['Guard', 'Forward', 'Center', 'Guard']
    })
    
    numeric_config = {
        'player_score': {
            'fill_method': 'median', 
            'min_value': 0, 
            'max_value': 50, 
            'convert_to': float
        }
    }
    
    categorical_config = {
        'team': {
            'fill_method': 'unknown',
            'lowercase': True
        },
        'player_position': {
            'fill_method': 'mode'
        }
    }
    
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_data(sample_data, numeric_config, categorical_config)
    print(cleaned_data)