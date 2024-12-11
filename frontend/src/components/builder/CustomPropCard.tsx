// components/builder/CustomPropCard.tsx
import React from 'react';
import { PropBet, PropType } from '../../types/props';

interface CustomPropCardProps {
  prop: PropBet;
}

export const CustomPropCard: React.FC<CustomPropCardProps> = ({ prop }) => {
  // Find the best odds (you might want to implement a more sophisticated selection logic)
  const bestOdds = prop.odds.length > 0 
    ? prop.odds.reduce((best, current) => 
        (current.probability > best.probability) ? current : best
      )
    : null;

  return (
    <div className="custom-prop-card bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4">{prop.playerName} Prop</h3>
      
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="font-medium">Prop Details:</span>
          <div>
            <span 
              className="ml-2 bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
            >
              {prop.category}: {prop.value}
            </span>
          </div>
        </div>
        
        {bestOdds && (
          <>
            <div className="flex justify-between border-t pt-3">
              <span className="font-medium">Probability:</span>
              <span className="text-green-600 font-bold">
                {(bestOdds.probability * 100).toFixed(2)}%
              </span>
            </div>
            
            <div className="flex justify-between border-t pt-3">
              <span className="font-medium">Recommended Odds:</span>
              <span className="text-blue-600 font-bold">
                {bestOdds.propType === PropType.OVER ? 'Over' : 'Under'} {bestOdds.value}
              </span>
            </div>
          </>
        )}

        {prop.valueIndicator && (
          <div className="flex justify-between border-t pt-3">
            <span className="font-medium">Value Indicator:</span>
            <span 
              className={`font-bold ${
                prop.valueIndicator === 'high' ? 'text-green-600' :
                prop.valueIndicator === 'medium' ? 'text-yellow-600' :
                'text-red-600'
              }`}
            >
              {prop.valueIndicator.toUpperCase()}
            </span>
          </div>
        )}
      </div>

      <button className="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
        Save Prop
      </button>
    </div>
  );
};