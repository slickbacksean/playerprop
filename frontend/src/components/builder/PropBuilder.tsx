import React, { useState, useCallback, useMemo } from 'react';
import { StatSelector } from './StatSelector';
import { OddsCalculator } from './OddsCalculator';
import { CustomPropCard } from './CustomPropCard';
import { usePropBuilder } from '../../hooks/usePropBuilder';
import { PropBet, PropCategory, PropType, PlayerStat, Odds } from '../../types/props';
import { v4 as uuidv4 } from 'uuid';

// Use the enum values directly
const PROP_CATEGORIES: PropCategory[] = [
  PropCategory.POINTS, 
  PropCategory.REBOUNDS, 
  PropCategory.ASSISTS, 
  PropCategory.STEALS, 
  PropCategory.BLOCKS, 
  PropCategory.THREES
];

export const PropBuilder: React.FC = () => {
  const propBuilder = usePropBuilder();
  
  // State for the current custom prop being built
  const [customProp, setCustomProp] = useState<PropBet | null>(null);
  
  // State to track available and selected categories
  const [availableCategories, setAvailableCategories] = useState<PropCategory[]>(PROP_CATEGORIES);
  
  // State to track selected stats
  const [selectedStats, setSelectedStats] = useState<PlayerStat[]>([]);

  // Initialize a new custom prop
  const handleCreateProp = useCallback(() => {
    if (selectedStats.length === 0) {
      alert('Please select at least one stat before creating a prop');
      return;
    }

    const newCustomProp: PropBet = {
      id: uuidv4(),
      playerId: '', 
      playerName: '',
      sport: 'basketball',
      category: selectedStats[0].category, 
      value: selectedStats[0].value,
      recommendedOdds: 1.5,
      odds: [], 
      probability: 0,
      timestamp: new Date().toISOString(),
      valueIndicator: 'medium',
      riskScore: 5 
    };

    setCustomProp(newCustomProp);
  }, [selectedStats]);

  // Handle stat selection
  const handleStatSelect = useCallback((stat: PlayerStat) => {
    // Prevent duplicates
    if (selectedStats.some(s => s.category === stat.category)) {
      alert('This stat category is already selected');
      return;
    }

    // Limit to max 2 stats
    if (selectedStats.length >= 2) {
      alert('You can only select up to 2 stats');
      return;
    }

    setSelectedStats(prev => [...prev, stat]);
    setAvailableCategories(prev => prev.filter(cat => cat !== stat.category));
  }, [selectedStats]);

  // Handle stat removal
  const handleStatRemove = useCallback((stat: PlayerStat) => {
    setSelectedStats(prev => prev.filter(s => s.category !== stat.category));
    setAvailableCategories(prev => [...prev, stat.category]);
  }, []);

  // Enhanced probability calculation
  const calculateProbability = useMemo(() => {
    if (selectedStats.length === 0) return 0;

    const baseProbability = 0.6;
    
    const categoryAdjustments = {
      [PropCategory.POINTS]: 1.0,
      [PropCategory.REBOUNDS]: 0.9,
      [PropCategory.ASSISTS]: 0.85,
      [PropCategory.STEALS]: 0.7,
      [PropCategory.BLOCKS]: 0.7,
      [PropCategory.THREES]: 0.8
    };

    // If multiple stats, slightly reduce probability
    const adjustmentFactor = selectedStats.length > 1 ? 0.9 : 1;

    const avgProbability = selectedStats.reduce((acc, stat) => {
      return acc * (categoryAdjustments[stat.category] || 1);
    }, baseProbability);

    return avgProbability * adjustmentFactor;
  }, [selectedStats]);

  // Odds calculation with more nuanced logic
  const getRecommendedOdds = useMemo(() => {
    const probability = calculateProbability;
    
    // Convert probability to decimal odds
    const decimalOdds = probability > 0 
      ? Number((1 / probability).toFixed(2)) 
      : 1.5;
    
    // Create a sample odds array
    const sampleOdds: Odds[] = [
      {
        bookmaker: 'FanDuel',
        propType: PropType.OVER,
        value: decimalOdds,
        probability: probability
      },
      {
        bookmaker: 'DraftKings',
        propType: PropType.UNDER,
        value: decimalOdds + 0.2,
        probability: 1 - probability
      }
    ];

    // Update the prop's odds if it exists
    if (customProp) {
      setCustomProp(prev => prev ? {...prev, odds: sampleOdds, probability} : null);
    }

    return decimalOdds.toFixed(2);
  }, [calculateProbability, customProp]);

  return (
    <div className="prop-builder p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Custom Prop Builder</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <StatSelector 
            availableStats={availableCategories}
            onStatSelect={handleStatSelect}
            onStatRemove={handleStatRemove}
            selectedStats={selectedStats}
          />
          <button 
            onClick={handleCreateProp}
            className="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
            disabled={customProp !== null || selectedStats.length === 0}
          >
            {customProp ? 'Prop Created' : 'Create Custom Prop'}
          </button>
        </div>
        
        <div>
          <OddsCalculator 
            selectedStats={selectedStats}
            calculateProbability={() => calculateProbability}
            getRecommendedOdds={() => getRecommendedOdds}
          />
        </div>
      </div>

      {customProp && (
        <div className="mt-6">
          <CustomPropCard prop={customProp} />
        </div>
      )}
    </div>
  );
};