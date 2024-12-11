import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

// Define color types explicitly
export type ProgressColor = 'primary' | 'success' | 'warning' | 'danger' | 'neutral';
export type ProgressSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

// Base progress variant configuration
const progressVariants = cva(
  'w-full h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 overflow-hidden transition-all duration-300 ease-in-out',
  {
    variants: {
      color: {
        primary: 'bg-blue-200 dark:bg-blue-900',
        success: 'bg-green-200 dark:bg-green-900',
        warning: 'bg-yellow-200 dark:bg-yellow-900',
        danger: 'bg-red-200 dark:bg-red-900',
        neutral: 'bg-gray-200 dark:bg-gray-700'
      },
      size: {
        xs: 'h-1',
        sm: 'h-2',
        md: 'h-2.5',
        lg: 'h-4',
        xl: 'h-5'
      },
      animated: {
        true: 'animate-pulse',
        false: ''
      }
    },
    defaultVariants: {
      color: 'primary',
      size: 'md',
      animated: false
    }
  }
);

const progressIndicatorVariants = cva(
  'h-full rounded-full transition-all duration-500 ease-in-out',
  {
    variants: {
      color: {
        primary: 'bg-blue-600 dark:bg-blue-500',
        success: 'bg-green-600 dark:bg-green-500',
        warning: 'bg-yellow-600 dark:bg-yellow-500',
        danger: 'bg-red-600 dark:bg-red-500',
        neutral: 'bg-gray-600 dark:bg-gray-500'
      }
    },
    defaultVariants: {
      color: 'primary'
    }
  }
);

export interface ProgressProps extends 
  Omit<React.HTMLAttributes<HTMLDivElement>, 'color'>, 
  VariantProps<typeof progressVariants>, 
  VariantProps<typeof progressIndicatorVariants> {
  value?: number;
  max?: number;
  label?: string;
  showPercentage?: boolean;
  indeterminate?: boolean;
}

const Progress: React.FC<ProgressProps> = ({
  value = 0,
  max = 100,
  color = 'primary',
  size = 'md',
  animated = false,
  label,
  showPercentage = false,
  indeterminate = false,
  className,
  ...props
}) => {
  // Ensure value is between 0 and max
  const clampedValue = Math.min(Math.max(value, 0), max);
  const percentage = ((clampedValue / max) * 100).toFixed(0);

  return (
    <div className="flex flex-col space-y-2 w-full">
      {(label || showPercentage) && (
        <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400">
          {label && <span>{label}</span>}
          {showPercentage && <span>{percentage}%</span>}
        </div>
      )}
      <div 
        role="progressbar"
        aria-valuenow={indeterminate ? undefined : Number(percentage)}
        aria-valuemin={0}
        aria-valuemax={100}
        className={progressVariants({ color, size, animated, className })}
        {...props}
      >
        {!indeterminate ? (
          <div 
            className={progressIndicatorVariants({ color })} 
            style={{ width: `${percentage}%` }}
          />
        ) : (
          <div className="w-1/3 h-full bg-blue-600/50 animate-indeterminate" />
        )}
      </div>
    </div>
  );
};

export default Progress;