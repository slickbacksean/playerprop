def create_categorical_encodings(self, df: pd.DataFrame, categorical_columns: List[str], encoding_type: str = 'onehot') -> pd.DataFrame:
        """
        Create categorical feature encodings.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            categorical_columns (List[str]): Columns to encode
            encoding_type (str): Encoding method ('onehot', 'label', or 'ordinal')
        
        Returns:
            pd.DataFrame: DataFrame with encoded categorical features
        """
        encoded_df = df.copy()
        
        if encoding_type == 'onehot':
            encoded_df = pd.get_dummies(encoded_df, columns=categorical_columns)
        
        elif encoding_type == 'label':
            from sklearn.preprocessing import LabelEncoder
            label_encoder = LabelEncoder()
            
            for column in categorical_columns:
                encoded_df[f'{column}_encoded'] = label_encoder.fit_transform(encoded_df[column].astype(str))
        
        elif encoding_type == 'ordinal':
            from sklearn.preprocessing import OrdinalEncoder
            ordinal_encoder = OrdinalEncoder()
            
            for column in categorical_columns:
                encoded_df[f'{column}_ordinal'] = ordinal_encoder.fit_transform(encoded_df[[column]])
        
        return encoded_df
    
    def engineer_features(self, 
                           df: pd.DataFrame, 
                           config: Dict[str, Any]) -> pd.DataFrame:
        """
        Comprehensive feature engineering pipeline.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            config (Dict): Feature engineering configuration
        
        Returns:
            pd.DataFrame: DataFrame with engineered features
        """
        engineered_df = df.copy()
        
        # Statistical features
        if config.get('statistical_features'):
            for stat_feature in config['statistical_features']:
                engineered_df = self.create_statistical_features(
                    engineered_df, 
                    stat_feature['group_columns'], 
                    stat_feature['target_column']
                )
        
        # Lag features
        if config.get('lag_features'):
            for lag_feature in config['lag_features']:
                engineered_df = self.create_lag_features(
                    engineered_df,
                    lag_feature['time_column'],
                    lag_feature['target_column'],
                    lag_feature.get('lags', [1, 2, 3])
                )
        
        # Ratio features
        if config.get('ratio_features'):
            for ratio_feature in config['ratio_features']:
                engineered_df = self.create_ratio_features(
                    engineered_df,
                    ratio_feature['numerator_column'],
                    ratio_feature['denominator_column']
                )
        
        # Categorical encodings
        if config.get('categorical_encoding'):
            engineered_df = self.create_categorical_encodings(
                engineered_df,
                config['categorical_encoding']['columns'],
                config['categorical_encoding'].get('type', 'onehot')
            )
        
        return engineered_df

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example DataFrame
    sample_data = pd.DataFrame({
        'player_id': [1, 1, 1, 2, 2],
        'game_date': pd.date_range(start='1/1/2023', periods=5),
        'player_score': [10.5, 12.3, 11.2, 15.6, 14.7],
        'team': ['Lakers', 'Lakers', 'Lakers', 'Bulls', 'Bulls'],
        'position': ['Guard', 'Guard', 'Guard', 'Forward', 'Forward']
    })
    
    # Feature engineering configuration
    feature_config = {
        'statistical_features': [
            {
                'group_columns': ['player_id'],
                'target_column': 'player_score'
            }
        ],
        'lag_features': [
            {
                'time_column': 'game_date',
                'target_column': 'player_score',
                'lags': [1, 2]
            }
        ],
        'ratio_features': [
            {
                'numerator_column': 'player_score',
                'denominator_column': 'player_id'
            }
        ],
        'categorical_encoding': {
            'columns': ['team', 'position'],
            'type': 'onehot'
        }
    }
    
    feature_engineer = FeatureEngineer()
    engineered_data = feature_engineer.engineer_features(sample_data, feature_config)
    print(engineered_data)