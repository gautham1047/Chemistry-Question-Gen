import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '../components/Header';
import { UnitCard } from '../components/UnitCard';

const Home = () => {
  const navigate = useNavigate();
  const [showOptionsPopup, setShowOptionsPopup] = useState(false);

  const units = [
    'All',
    'Intro to Chemistry',
    'Atomic Structure',
    'Periodic Table',
    'Bonding',
    'Reactions',
    'Stoichiometry',
    'Gas Laws',
    'Solutions',
    'Acids and Bases',
    'Thermochemistry',
    'Kinetics',
    'Equilibrium',
    'Electrochemistry',
    'Organic Chemistry',
    'Nuclear Chemistry',
  ];

  const [selectedUnits, setSelectedUnits] = useState<Set<number>>(new Set([0]));

  const handleUnitToggle = (index: number) => {
    setSelectedUnits((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  const handleStart = () => {
    setShowOptionsPopup(true);
  };

  const handleOptionSelect = (option: 'test' | 'single') => {
    setShowOptionsPopup(false);
    if (option === 'test') {
      navigate('/batch-questions');
    } else {
      const randomId = Math.floor(Math.random() * 74) + 1;
      navigate(`/question/${randomId}`);
    }
  };

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />

      <main className="container mx-auto px-8 py-12">
        <div className="grid grid-cols-4 gap-6 mb-12">
          {units.map((unit, index) => (
            <UnitCard
              key={index}
              unitName={unit}
              isSelected={selectedUnits.has(index)}
              onToggle={() => handleUnitToggle(index)}
            />
          ))}
        </div>

        <div className="flex justify-center items-center gap-4 pb-8">
          <button
            onClick={handleStart}
            className="bg-highlight hover:bg-highlight-alt text-text-primary font-semibold px-12 py-4 rounded-lg transition-colors text-lg flex-1 max-w-md"
          >
            Start
          </button>
          <button
            onClick={() => setShowOptionsPopup(!showOptionsPopup)}
            className="bg-bg-secondary hover:opacity-70 text-text-primary px-6 py-4 rounded-lg transition-opacity border-2 border-text-secondary"
            aria-label="Options"
          >
            ⋮
          </button>
        </div>

        {showOptionsPopup && (
          <>
            <div
              className="fixed inset-0 bg-black bg-opacity-50 z-40"
              onClick={() => setShowOptionsPopup(false)}
            />
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-bg-secondary border-2 border-text-secondary rounded-lg shadow-2xl p-6 z-50 min-w-80">
              <h3 className="text-text-primary text-xl font-semibold mb-4">Select Mode</h3>
              <div className="flex flex-col gap-3">
                <button
                  onClick={() => handleOptionSelect('test')}
                  className="bg-highlight hover:bg-highlight-alt text-text-primary px-6 py-3 rounded-lg transition-colors"
                >
                  Test
                </button>
                <button
                  onClick={() => handleOptionSelect('single')}
                  className="bg-highlight hover:bg-highlight-alt text-text-primary px-6 py-3 rounded-lg transition-colors"
                >
                  Single Question
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
};

export default Home;
