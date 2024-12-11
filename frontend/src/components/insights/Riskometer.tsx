import React from 'react';
import Progress, { ProgressColor } from '../ui/progress';
import { 
  AlertTriangle, 
  ShieldCheck, 
  AlertCircle 
} from 'lucide-react';

interface RiskometerProps {
  riskScore: number; // 0-100
}

const Riskometer: React.FC<RiskometerProps> = ({ riskScore }) => {
  const getRiskLabel = () => {
    if (riskScore <= 30) return 'Low Risk';
    if (riskScore <= 70) return 'Moderate Risk';
    return 'High Risk';
  };

  const getRiskIcon = () => {
    if (riskScore <= 30) 
      return <ShieldCheck className="text-green-500" />;
    if (riskScore <= 70) 
      return <AlertTriangle className="text-yellow-500" />;
    return <AlertCircle className="text-red-500" />;
  };

  const getRiskColor = (): ProgressColor => {
    if (riskScore <= 30) return 'success';
    if (riskScore <= 70) return 'warning';
    return 'danger';
  };

  return (
    <div className="flex flex-col space-y-2 p-4 border rounded-lg">
      <div className="flex items-center justify-between">
        <span className="font-semibold">Risk Assessment</span>
        {getRiskIcon()}
      </div>
      <Progress 
        value={riskScore} 
        color={getRiskColor()}
        showPercentage
      />
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>Low</span>
        <span>{getRiskLabel()} ({riskScore}%)</span>
        <span>High</span>
      </div>
    </div>
  );
};

export default Riskometer;