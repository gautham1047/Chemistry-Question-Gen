import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'accent';
  type?: 'button' | 'submit';
  disabled?: boolean;
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  type = 'button',
  disabled = false,
  className = '',
}) => {
  const base =
    'inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors cursor-pointer select-none';

  const variants = {
    primary: 'bg-cyan-600 hover:bg-cyan-500 text-white',
    secondary: 'bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600',
    accent: 'bg-emerald-600 hover:bg-emerald-500 text-white',
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {label}
    </button>
  );
};

export default Button;
