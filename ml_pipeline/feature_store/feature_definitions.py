from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

@dataclass
class FeatureDefinition:
    """
    Comprehensive feature definition for machine learning features
    """
    name: str
    description: str
    data_type: str
    source: str
    transformation: Optional[str] = None
    preprocessing_steps: List[str] = field(default_factory=list)
    statistical_properties: Dict[str, Any] = field(default_factory=dict)
    importance_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert feature definition to dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation of feature
        """
        return {
            "name": self.name,
            "description": self.description,
            "data_type": self.data_type,
            "source": self.source,
            "transformation": self.transformation,
            "preprocessing_steps": self.preprocessing_steps,
            "statistical_properties": self.statistical_properties,
            "importance_score": self.importance_score
        }

class FeatureDefinitionRegistry:
    """
    Registry for managing and organizing feature definitions
    """
    def __init__(self):
        self._features: Dict[str, FeatureDefinition] = {}
    
    def register_feature(self, feature: FeatureDefinition):
        """
        Register a new feature definition
        
        Args:
            feature (FeatureDefinition): Feature to register
        """
        self._features[feature.name] = feature
    
    def get_feature(self, name: str) -> Optional[FeatureDefinition]:
        """
        Retrieve a feature definition
        
        Args:
            name (str): Name of the feature
        
        Returns:
            Optional[FeatureDefinition]: Feature definition or None
        """
        return self._features.get(name)
    
    def list_features(self) -> List[str]:
        """
        List all registered feature names
        
        Returns:
            List[str]: List of feature names
        """
        return list(self._features.keys())
    
    def export_to_json(self, filepath: str):
        """
        Export feature definitions to JSON
        
        Args:
            filepath (str): Path to save JSON file
        """
        feature_dict = {name: feature.to_dict() for name, feature in self._features.items()}
        with open(filepath, 'w') as f:
            json.dump(feature_dict, f, indent=4)

# Example usage and predefined sports features
if __name__ == "__main__":
    registry = FeatureDefinitionRegistry()
    
    # Player Performance Features
    player_score_feature = FeatureDefinition(
        name="player_score",
        description="Total points scored by a player in a game",
        data_type="float",
        source="game_statistics",
        transformation="rolling_mean",
        preprocessing_steps=[
            "handle_missing_values",
            "normalize"
        ],
        statistical_properties={
            "mean": None,
            "std": None,
            "min": 0,
            "max": 50
        }
    )
    
    # Team Performance Features
    team_win_rate_feature = FeatureDefinition(
        name="team_win_rate",
        description="Percentage of games won by a team",
        data_type="float",
        source="team_history",
        transformation="cumulative_average",
        preprocessing_steps=[
            "handle_outliers",
            "standardize"
        ]
    )
    
    registry.register_feature(player_score_feature)
    registry.register_feature(team_win_rate_feature)
    
    # Export to JSON for reference
    registry.export_to_json("feature_definitions.json")