import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/var/log/ml_pipeline/feature_engineering.log'
)
logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    A comprehensive feature engineering class for sports prop predictions
    with robust logging and error handling.
    """
    
    def __init__(self, feature_registry_path: str = 'ml_pipeline/feature_store/feature_registry.json'):
        """
        Initialize the FeatureEngineer with feature registry configuration.
        
        Args:
            feature_registry_path (str): Path to the feature registry JSON file
        """
        try:
            with open(feature_registry_path, 'r') as f:
                self.feature_registry = json.load(f)
            
            logger.info(f"Feature registry loaded successfully from {feature_registry_path}")
        except FileNotFoundError:
            logger.error(f"Feature registry file not found: {feature_registry_path}")
            self.feature_registry = {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in feature registry file: {feature_registry_path}")
            self.feature_registry = {}

    def _validate_input(self, df: pd.DataFrame) -> bool:
        """
        Validate input DataFrame against expected columns and data types.
        
        Args:
            df (pd.DataFrame): Input DataFrame to validate
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        required_columns = self.feature_registry.get('required_columns', [])
        
        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.warning(f"Missing required columns: {missing_columns}")
            return False
        
        # Optional: Add type checking
        try:
            for col, expected_type in self.feature_registry.get('column_types', {}).items():
                if col in df.columns:
                    if expected_type == 'numeric':
                        pd.to_numeric(df[col], errors='raise')
                    elif expected_type == 'datetime':
                        pd.to_datetime(df[col], errors='raise')
            return True
        except (TypeError, ValueError) as e:
            logger.error(f"Type validation failed: {e}")
            return False

    def create_time_based_features(self, df: pd.DataFrame, date_column: str = 'game_date') -> pd.DataFrame:
        """
        Generate time-based features for sports prop predictions.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_column (str): Name of the date column to use
        
        Returns:
            pd.DataFrame: DataFrame with additional time-based features
        """
        if not self._validate_input(df):
            logger.warning("Input validation failed for time-based feature generation")
            return df

        try:
            df[date_column] = pd.to_datetime(df[date_column])
            
            # Time-based features
            df['day_of_week'] = df[date_column].dt.dayofweek
            df['month'] = df[date_column].dt.month
            df['season'] = self._determine_season(df[date_column])
            
            # Time since last game (assuming sorted DataFrame)
            df['days_since_last_game'] = df[date_column].diff().dt.days
            
            logger.info("Successfully generated time-based features")
            return df
        
        except Exception as e:
            logger.error(f"Error generating time-based features: {e}")
            return df

    def _determine_season(self, dates: pd.Series) -> pd.Series:
        """
        Determine sports season based on date.
        
        Args:
            dates (pd.Series): Series of dates
        
        Returns:
            pd.Series: Season labels
        """
        def get_season(date):
            year = date.year
            if date.month >= 9 and date.month <= 12:
                return f'{year}-{year+1} Season'
            elif date.month >= 1 and date.month <= 4:
                return f'{year-1}-{year} Season'
            else:
                return 'Off Season'
        
        return dates.apply(get_season)

    def calculate_rolling_statistics(
        self, 
        df: pd.DataFrame, 
        group_column: str, 
        value_column: str, 
        windows: List[int] = [3, 5, 10]
    ) -> pd.DataFrame:
        """
        Calculate rolling statistics for performance tracking.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            group_column (str): Column to group by (e.g., player or team)
            value_column (str): Column to calculate statistics on
            windows (List[int]): Rolling window sizes
        
        Returns:
            pd.DataFrame: DataFrame with rolling statistics
        """
        if not self._validate_input(df):
            logger.warning("Input validation failed for rolling statistics")
            return df

        try:
            # Sort DataFrame to ensure correct rolling calculations
            df_sorted = df.sort_values(by=['game_date', group_column])
            
            for window in windows:
                # Rolling mean
                df[f'{value_column}_rolling_mean_{window}'] = df_sorted.groupby(group_column)[value_column].rolling(window=window, min_periods=1).mean().reset_index(0, drop=True)
                
                # Rolling standard deviation
                df[f'{value_column}_rolling_std_{window}'] = df_sorted.groupby(group_column)[value_column].rolling(window=window, min_periods=1).std().reset_index(0, drop=True)
            
            logger.info(f"Generated rolling statistics for {value_column} with windows: {windows}")
            return df
        
        except Exception as e:
            logger.error(f"Error calculating rolling statistics: {e}")
            return df

    def detect_and_handle_outliers(
        self, 
        df: pd.DataFrame, 
        column: str, 
        method: str = 'zscore', 
        threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Detect and optionally handle outliers in a given column.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            column (str): Column to check for outliers
            method (str): Outlier detection method ('zscore' or 'iqr')
            threshold (float): Threshold for outlier detection
        
        Returns:
            pd.DataFrame: DataFrame with outliers handled
        """
        try:
            if method == 'zscore':
                mean = df[column].mean()
                std = df[column].std()
                z_scores = np.abs((df[column] - mean) / std)
                outliers = z_scores > threshold
            
            elif method == 'iqr':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - (threshold * IQR)
                upper_bound = Q3 + (threshold * IQR)
                outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
            
            else:
                logger.warning(f"Unsupported outlier method: {method}")
                return df
            
            # Log outlier information
            outlier_count = outliers.sum()
            outlier_percentage = (outlier_count / len(df)) * 100
            
            logger.info(f"Outlier detection for {column}: {outlier_count} outliers ({outlier_percentage:.2f}%)")
            
            # Option to cap outliers instead of removing
            df.loc[outliers, column] = df.loc[~outliers, column].median()
            
            return df
        
        except Exception as e:
            logger.error(f"Error detecting outliers in {column}: {e}")
            return df

    def save_feature_metadata(self, features: Dict[str, Any], output_path: Optional[str] = None):
        """
        Save feature metadata to track feature engineering process.
        
        Args:
            features (Dict): Dictionary of generated features
            output_path (str, optional): Path to save feature metadata
        """
        if output_path is None:
            output_path = 'ml_pipeline/feature_store/feature_metadata.json'
        
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'feature_count': len(features)
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            logger.info(f"Feature metadata saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save feature metadata: {e}")

def main():
    """
    Example usage of FeatureEngineer class
    """
    # Example initialization
    feature_engineer = FeatureEngineer()
    
    # Load sample data (replace with actual data loading)
    try:
        df = pd.read_csv('path/to/sports/data.csv')
        
        # Apply feature engineering steps
        df = feature_engineer.create_time_based_features(df)
        df = feature_engineer.calculate_rolling_statistics(df, 'player_name', 'performance_score')
        df = feature_engineer.detect_and_handle_outliers(df, 'performance_score')
        
        # Optional: Save processed features
        feature_engineer.save_feature_metadata(df.columns.tolist())
        
        logger.info("Feature engineering completed successfully")
    
    except Exception as e:
        logger.error(f"Feature engineering pipeline failed: {e}")

if __name__ == "__main__":
    main()