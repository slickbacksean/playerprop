import React from 'react';
import { cva, VariantProps } from 'class-variance-authority';

// Card variants configuration
const cardVariants = cva(
  'rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-300 ease-in-out',
  {
    variants: {
      variant: {
        default: 'border-border',
        elevated: 'hover:shadow-lg',
        outline: 'border-2 border-primary/50',
        ghost: 'border-transparent hover:bg-accent'
      },
      size: {
        sm: 'p-2',
        md: 'p-4',
        lg: 'p-6'
      }
    },
    defaultVariants: {
      variant: 'default',
      size: 'md'
    }
  }
);

export interface CardProps extends 
  React.HTMLAttributes<HTMLDivElement>, 
  VariantProps<typeof cardVariants> {
  children: React.ReactNode;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, size, children, ...props }, ref) => {
    return (
      <div 
        ref={ref}
        className={cardVariants({ variant, size, className })}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement, 
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div 
    ref={ref}
    className={`flex flex-col space-y-1.5 p-4 ${className}`}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLHeadingElement, 
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3 
    ref={ref}
    className={`text-lg font-semibold leading-none tracking-tight ${className}`}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLParagraphElement, 
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p 
    ref={ref}
    className={`text-sm text-muted-foreground ${className}`}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<
  HTMLDivElement, 
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div 
    ref={ref}
    className={`p-4 pt-0 ${className}`}
    {...props}
  />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<
  HTMLDivElement, 
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div 
    ref={ref}
    className={`flex items-center p-4 pt-0 ${className}`}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent, 
  CardFooter 
};

// Example Usage Component
export const CardExamples: React.FC = () => {
  return (
    <div className="space-y-4 p-4">
      <Card variant="elevated">
        <CardHeader>
          <CardTitle>Project Overview</CardTitle>
          <CardDescription>
            Detailed insights into your current project
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>Status: Active</div>
            <div>Progress: 75%</div>
          </div>
        </CardContent>
        <CardFooter>
          <button className="w-full bg-primary text-primary-foreground py-2 rounded">
            View Details
          </button>
        </CardFooter>
      </Card>
    </div>
  );
};