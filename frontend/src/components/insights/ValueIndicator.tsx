import React from 'react';
import { Badge } from '../ui/badge';
import { 
  TrendingUp, 
  TrendingDown, 
  Scale 
} from 'lucide-react';

interface ValueIndicatorProps {
  value: number;
  type: 'undervalued' | 'overvalued' | 'neutral';
  confidence: number;
  propDetails?: {
    player: string;
    sport: string;
    metric: string;
  };
}

const ValueIndicator: React.FC<ValueIndicatorProps> = ({ 
  value, 
  type, 
  confidence, 
  propDetails 
}) => {
  const getVariant = () => {
    switch (type) {
      case 'undervalued':
        return 'green';
      case 'overvalued':
        return 'red';
      default:
        return 'outline';
    }
  };

  const getTypeIcon = () => {
    switch (type) {
      case 'undervalued':
        return <TrendingUp className="w-4 h-4 mr-2" />;
      case 'overvalued':
        return <TrendingDown className="w-4 h-4 mr-2" />;
      default:
        return <Scale className="w-4 h-4 mr-2" />;
    }
  };

  const getConfidenceDescription = () => {
    if (confidence < 0.3) return 'Low Confidence';
    if (confidence < 0.7) return 'Moderate Confidence';
    return 'High Confidence';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <Badge variant={getVariant()} className="flex items-center">
            {getTypeIcon()}
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </Badge>
          <div className="ml-3 text-sm text-muted-foreground">
            Value: {value.toFixed(2)}
          </div>
        </div>
        {propDetails && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {propDetails.player} | {propDetails.sport}
          </div>
        )}
      </div>
      
      <div className="flex justify-between items-center">
        <div className="text-xs text-gray-600 dark:text-gray-300">
          Confidence: {(confidence * 100).toFixed(0)}% 
          <span className="ml-2 text-muted-foreground">
            ({getConfidenceDescription()})
          </span>
        </div>
        {propDetails && (
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Metric: {propDetails.metric}
          </div>
        )}
      </div>
    </div>
  );
};

export default ValueIndicator;