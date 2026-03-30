import { useState, useRef, useEffect } from 'react';

interface UnitCardProps {
  unitName: string;
  imageUrl?: string;
  isSelected: boolean;
  onToggle: () => void;
}

export const UnitCard = ({ unitName, imageUrl, isSelected, onToggle }: UnitCardProps) => {
  const [isPeeled, setIsPeeled] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (cardRef.current && !cardRef.current.contains(event.target as Node)) {
        setIsPeeled(false);
      }
    };

    if (isPeeled) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isPeeled]);

  const handleDogEarClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsPeeled(!isPeeled);
  };

  return (
    <div ref={cardRef} className="relative w-64 h-48 perspective-1000">
      <div
        className={`relative w-full h-full transition-transform duration-500 transform-style-3d ${
          isPeeled ? 'rotate-y-12' : ''
        }`}
      >
        {/* Main Card */}
        <div
          className="absolute inset-0 bg-highlight rounded-lg shadow-lg cursor-pointer overflow-hidden"
          onClick={onToggle}
        >
          {/* Image Area */}
          {imageUrl && (
            <div className="w-full h-32 bg-bg-secondary flex items-center justify-center">
              <img src={imageUrl} alt={unitName} className="max-w-full max-h-full object-contain" />
            </div>
          )}
          {!imageUrl && <div className="w-full h-32 bg-bg-secondary" />}

          {/* Unit Name */}
          <div className="absolute bottom-4 right-4 text-text-primary font-semibold text-lg">
            {unitName}
          </div>

          {/* Dog-ear fold indicator */}
          <div
            className="absolute top-0 right-0 w-0 h-0 border-l-[40px] border-l-transparent border-t-[40px] border-t-text-secondary cursor-pointer hover:border-t-highlight-alt transition-colors"
            onClick={handleDogEarClick}
          />

          {/* Selection indicator */}
          {isSelected && (
            <div className="absolute top-2 left-2 w-6 h-6 bg-highlight-alt rounded-full flex items-center justify-center">
              <span className="text-bg-secondary text-sm font-bold">✓</span>
            </div>
          )}
        </div>

        {/* Peeled Options Menu - Currently placeholder */}
        {isPeeled && (
          <div className="absolute inset-0 bg-bg-secondary rounded-lg shadow-2xl p-4 overflow-y-auto z-10">
            <div className="text-text-primary text-sm">
              <p className="mb-2 font-semibold">Question Types:</p>
              <p className="text-xs opacity-70">
                Configure question types in Settings
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
