import React, { useState, useMemo } from 'react';
import { PlayerStat, PropCategory } from '../../types/props';

export interface StatSelectorProps {
  availableStats: PropCategory[];
  onStatSelect: (stat: PlayerStat) => void;
  onStatRemove: (stat: PlayerStat) => void;
  selectedStats: PlayerStat[];
}

export const StatSelector: React.FC<StatSelectorProps> = ({
  availableStats,
  onStatSelect,
  onStatRemove,
  selectedStats
}) => {
  const [inputValue, setInputValue] = useState<number>(0);
  const [selectedCategory, setSelectedCategory] = useState<PropCategory>(
    availableStats.length > 0 ? availableStats[0] : PropCategory.POINTS
  );

  // Validate input value
  const isValidInput = useMemo(() => {
    return inputValue > 0;
  }, [inputValue]);

  const handleSelect = () => {
    // Additional validation
    if (!isValidInput) {
      alert('Please enter a valid stat value greater than 0');
      return;
    }

    const newStat: PlayerStat = {
      playerId: '',
      playerName: '',
      category: selectedCategory,
      value: inputValue,
      season: new Date().getFullYear()
    };
    
    onStatSelect(newStat);
    setInputValue(0);
  };

  return (
    <div className="space-y-4">
      <div>
        <label htmlFor="stat-category" className="block text-sm font-medium text-gray-700">
          Select Stat Category
        </label>
        <select
          id="stat-category"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value as PropCategory)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          disabled={availableStats.length === 0}
        >
          {availableStats.map((category) => (
            <option key={category} value={category}>
              {category.charAt(0).toUpperCase() + category.slice(1).toLowerCase()}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="stat-value" className="block text-sm font-medium text-gray-700">
          Enter Stat Value
        </label>
        <input
          id="stat-value"
          type="number"
          min="0"
          value={inputValue}
          onChange={(e) => setInputValue(Number(e.target.value))}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
        />
      </div>

      <button
        onClick={handleSelect}
        className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
        disabled={!isValidInput || availableStats.length === 0}
      >
        Add Stat
      </button>

      <div>
        <h3 className="text-lg font-semibold mb-2">Selected Stats</h3>
        {selectedStats.length > 0 ? (
          selectedStats.map((stat, index) => (
            <div key={index} className="flex justify-between items-center bg-gray-100 p-2 rounded-md mb-2">
              <span>
                {stat.category.charAt(0).toUpperCase() + stat.category.slice(1).toLowerCase()}:
                {' '}{stat.value}
              </span>
              <button
                onClick={() => onStatRemove(stat)}
                className="text-red-500 hover:text-red-700"
              >
                Remove
              </button>
            </div>
          ))
        ) : (
          <p className="text-gray-500">No stats selected</p>
        )}
      </div>
    </div>
  );
};