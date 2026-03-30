import React from 'react';

interface CheckboxProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

const Checkbox: React.FC<CheckboxProps> = ({ label, checked, onChange }) => {
  return (
    <label className="flex items-center cursor-pointer mb-3 pl-9 relative text-dark-olive font-sans text-base select-none">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="absolute opacity-0 cursor-pointer h-0 w-0 peer"
      />
      <span className="absolute left-0 top-0 h-6 w-6 bg-cream border-2 border-border-dark peer-checked:bg-teal peer-checked:border-teal after:content-[''] after:absolute after:hidden peer-checked:after:block after:left-[7px] after:top-[3px] after:w-[6px] after:h-[11px] after:border-white after:border-r-[3px] after:border-b-[3px] after:rotate-45"></span>
      {label}
    </label>
  );
};

export default Checkbox;
