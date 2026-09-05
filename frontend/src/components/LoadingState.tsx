import React from 'react';
import { Card } from './Card';

interface LoadingStateProps {
  message?: string;
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Loading...',
  className = '',
}) => {
  return (
    <Card className={`text-center text-slate-400 py-16 ${className}`}>
      <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
      <p className="text-sm font-medium">{message}</p>
    </Card>
  );
};

export default LoadingState;
