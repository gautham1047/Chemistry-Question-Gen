import React, { type ReactNode, type HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  variant?: 'default' | 'sm' | 'emerald' | 'subtle' | 'interactive';
  selected?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  selected = false,
  className = '',
  onClick,
  ...props
}) => {
  const baseVariants = {
    default: 'bg-slate-800 border border-slate-700 p-6 shadow-sm',
    sm: 'bg-slate-800 border border-slate-700 p-4 shadow-sm',
    emerald: 'bg-emerald-950/30 border border-emerald-500/40 p-5 shadow-sm',
    subtle: 'bg-slate-900/60 border border-slate-700 p-4 shadow-sm',
    interactive: 'bg-slate-900/80 border border-slate-700 hover:border-slate-500 p-4 transition-colors cursor-pointer select-none',
  };

  const selectedClass = selected
    ? '!bg-slate-800 !border-cyan-500 text-slate-100'
    : '';

  return (
    <div
      onClick={onClick}
      className={`${baseVariants[variant]} ${selectedClass} ${onClick && variant !== 'interactive' ? 'cursor-pointer' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const Box = Card;
export default Card;
