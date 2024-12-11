import React from 'react';
import { PlayerStat } from '../../types/props';

interface OddsCalculatorProps {
  selectedStats: PlayerStat[];
  calculateProbability: () => number;
  getRecommendedOdds: () => string;
}

export const OddsCalculator: React.FC<OddsCalculatorProps> = ({ 
  selectedStats, 
  calculateProbability,
  getRecommendedOdds 
}) => {
  const probability = calculateProbability();
  const recommendedOdds = getRecommendedOdds();

  return (
    <div className="odds-calculator bg-gray-50 p-4 rounded-lg">
      <h3 className="text-xl font-semibold mb-4">Prop Odds Analysis</h3>
      
      {selectedStats.length > 0 ? (
        <>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-3 rounded shadow">
              <h4 className="text-sm font-medium text-gray-600">Probability</h4>
              <p className="text-2xl font-bold text-blue-600">
                {(probability * 100).toFixed(2)}%
              </p>
            </div>
            
            <div className="bg-white p-3 rounded shadow">
              <h4 className="text-sm font-medium text-gray-600">Recommended Odds</h4>
              <p className="text-2xl font-bold text-green-600">
                {recommendedOdds}
              </p>
            </div>
          </div>

          <div className="mt-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Selected Stats:</h4>
            {selectedStats.map((stat, index) => (
              <div key={index} className="text-sm text-gray-500">
                {stat.category}: {stat.value}
              </div>
            ))}
          </div>
        </>
      ) : (
        <p className="text-gray-500 text-center">
          Select stats to calculate probabilities and odds
        </p>
      )}

      <div className="mt-4">
        <p className="text-xs text-gray-500">
          These probabilities are dynamically calculated based on selected stats and 
          historical player performance.
        </p>
      </div>
    </div>
  );
};