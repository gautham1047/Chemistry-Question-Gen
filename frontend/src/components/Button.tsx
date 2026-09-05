import React, { type ReactNode, type ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  label?: string;
  children?: ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'outline' | 'ghost';
  size?: 'sm' | 'md';
}

export const Button: React.FC<ButtonProps> = ({
  label,
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  type = 'button',
  disabled = false,
  className = '',
  ...props
}) => {
  const sizes = {
    sm: 'px-2.5 py-1 text-xs',
    md: 'px-4 py-2 text-sm',
  };

  const variants = {
    primary: 'bg-cyan-600 hover:bg-cyan-500 text-white font-medium',
    secondary: 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600 font-medium',
    accent: 'bg-emerald-600 hover:bg-emerald-500 text-white font-medium',
    outline: 'bg-transparent hover:bg-slate-800 text-slate-300 border border-slate-700 font-medium',
    ghost: 'bg-transparent hover:bg-slate-800/80 text-cyan-400 hover:text-cyan-300 font-medium',
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center cursor-pointer select-none transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${sizes[size]} ${variants[variant]} ${className}`}
      {...props}
    >
      {children || label}
    </button>
  );
};

export default Button;
