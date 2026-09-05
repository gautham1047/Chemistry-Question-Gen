import React, { type ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'cyan' | 'slate' | 'emerald';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'cyan',
  className = '',
}) => {
  const variants = {
    cyan: 'font-mono text-xs uppercase tracking-wider text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2 py-0.5',
    slate: 'text-xs text-slate-400 bg-slate-700/50 px-2 py-0.5',
    emerald: 'font-mono text-xs uppercase tracking-wider text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2 py-0.5',
  };

  return (
    <span className={`inline-flex items-center ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;
