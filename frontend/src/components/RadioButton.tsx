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
    <label className="flex items-center gap-2.5 py-1.5 cursor-pointer text-sm text-slate-200 select-none">
      <input
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onChange={() => onChange(value)}
        className="w-4 h-4 border-slate-600 bg-slate-800 text-cyan-500 accent-cyan-500 cursor-pointer"
      />
      <span>{label}</span>
    </label>
  );
};

export default RadioButton;
