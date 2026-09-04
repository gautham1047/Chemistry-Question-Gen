import React from 'react';

interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

const Checkbox: React.FC<CheckboxProps> = ({ label, checked, onChange }) => {
  return (
    <label className="flex items-center gap-2.5 py-1.5 cursor-pointer text-sm text-slate-200 select-none">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="w-4 h-4 border-slate-600 bg-slate-800 text-cyan-500 accent-cyan-500 cursor-pointer"
      />
      <span>{label}</span>
    </label>
  );
};

export default Checkbox;
