import React from 'react';
import { 
  Tooltip as BaseTooltip, 
  TooltipContent, 
  TooltipProvider, 
  TooltipTrigger 
} from '@radix-ui/react-tooltip';
import { cva, VariantProps } from 'class-variance-authority';

// Tooltip variant configuration
const tooltipVariants = cva(
  'z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
  {
    variants: {
      color: {
        default: 'bg-popover text-popover-foreground',
        primary: 'bg-primary text-primary-foreground',
        success: 'bg-green-500 text-white',
        warning: 'bg-yellow-500 text-black',
        danger: 'bg-red-500 text-white'
      },
      size: {
        sm: 'px-2 py-1 text-xs',
        md: 'px-3 py-1.5 text-sm',
        lg: 'px-4 py-2 text-base'
      }
    },
    defaultVariants: {
      color: 'default',
      size: 'md'
    }
  }
);

export interface TooltipProps extends 
  React.ComponentPropsWithoutRef<typeof BaseTooltip>, 
  VariantProps<typeof tooltipVariants> {
  content: React.ReactNode;
  children: React.ReactNode;
  delay?: number;
}

const Tooltip: React.FC<TooltipProps> = ({
  children,
  content,
  color = 'default',
  size = 'md',
  delay = 300,
  ...props
}) => {
  return (
    <TooltipProvider delayDuration={delay}>
      <BaseTooltip {...props}>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>
        <TooltipContent 
          className={tooltipVariants({ color, size })}
        >
          {content}
        </TooltipContent>
      </BaseTooltip>
    </TooltipProvider>
  );
};

// Example Usage Component
export const TooltipExamples: React.FC = () => {
  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center space-x-4">
        <Tooltip content="Default Tooltip">
          <button className="bg-gray-200 px-4 py-2 rounded">
            Hover me
          </button>
        </Tooltip>

        <Tooltip 
          content="Success Tooltip" 
          color="success"
          size="lg"
        >
          <button className="bg-green-200 px-4 py-2 rounded">
            Success
          </button>
        </Tooltip>

        <Tooltip 
          content="Warning Tooltip" 
          color="warning"
        >
          <button className="bg-yellow-200 px-4 py-2 rounded">
            Warning
          </button>
        </Tooltip>
      </div>
    </div>
  );
};

export { 
  Tooltip, 
  TooltipContent, 
  TooltipProvider, 
  TooltipTrigger 
};