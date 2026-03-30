import React from 'react';

interface RadioButtonProps {
  label: string;
  value: string | number;
  checked: boolean;
  onChange: (value: string | number) => void;
  name: string;
}

const RadioButton: React.FC<RadioButtonProps> = ({ label, value, checked, onChange, name }) => {
  return (
    <label className="flex items-center cursor-pointer mb-3 pl-9 relative text-dark-olive font-sans text-base select-none">
      <input
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onChange={() => onChange(value)}
        className="absolute opacity-0 cursor-pointer h-0 w-0 peer"
      />
      <span className="absolute left-0 top-0 h-6 w-6 bg-cream border-2 border-border-dark rounded-full peer-checked:bg-teal peer-checked:border-teal after:content-[''] after:absolute after:hidden peer-checked:after:block after:left-1/2 after:top-1/2 after:-translate-x-1/2 after:-translate-y-1/2 after:w-2 after:h-2 after:rounded-full after:bg-white"></span>
      {label}
    </label>
  );
};

export default RadioButton;
