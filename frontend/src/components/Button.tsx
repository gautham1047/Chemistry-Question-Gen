interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  type?: 'button' | 'submit';
  disabled?: boolean;
}

const Button = ({
  label,
  onClick,
  variant = 'primary',
  type = 'button',
  disabled = false,
}: ButtonProps) => {
  const baseStyles = 'px-8 py-3 text-base font-sans cursor-pointer transition-colors duration-200 rounded-lg';
  const variantStyles = variant === 'primary'
    ? 'bg-highlight hover:bg-highlight-alt text-text-primary'
    : 'bg-bg-secondary hover:opacity-70 text-text-primary border-2 border-text-secondary';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {label}
    </button>
  );
};

export default Button;
