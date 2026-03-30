import React from 'react';

interface SliderProps {
  min: number;
  max: number;
  value: number;
  onChange: (value: number) => void;
  label: string;
}

const Slider: React.FC<SliderProps> = ({ min, max, value, onChange, label }) => {
  return (
    <div className="w-full max-w-md">
      <div className="mb-2 text-dark-olive font-sans">
        {label}: <span className="font-bold">{value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-2 bg-sage-medium rounded-lg appearance-none cursor-pointer accent-teal"
      />
    </div>
  );
};

export default Slider;
