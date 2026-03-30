import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import Checkbox from '../components/Checkbox';
import RadioButton from '../components/RadioButton';

const Settings = () => {
  const navigate = useNavigate();
  const { state, updateSettings } = useAppContext();

  const [reactionTypes, setReactionTypes] = useState({
    synthesis: state.settings.reactionTypes.includes('synthesis'),
    decomposition: state.settings.reactionTypes.includes('decomposition'),
    combustion: state.settings.reactionTypes.includes('combustion'),
    singleReplacement: state.settings.reactionTypes.includes('single replacement'),
    doubleReplacement: state.settings.reactionTypes.includes('double replacement'),
  });

  const [polyatomicLevel, setPolyatomicLevel] = useState(state.settings.polyatomicLevel);
  const [unit, setUnit] = useState(state.settings.unit);

  useEffect(() => {
    // Fetch polyatomic choices when level changes
    const fetchPolyatomicChoices = async () => {
      try {
        const choices = await api.getPolyatomicChoices(polyatomicLevel);
        updateSettings({ polyatomicChoices: choices });
      } catch (err) {
        console.error('Failed to fetch polyatomic choices:', err);
      }
    };

    fetchPolyatomicChoices();
  }, [polyatomicLevel]);

  const handleSave = () => {
    const selectedReactionTypes: string[] = [];
    if (reactionTypes.synthesis) selectedReactionTypes.push('synthesis');
    if (reactionTypes.decomposition) selectedReactionTypes.push('decomposition');
    if (reactionTypes.combustion) selectedReactionTypes.push('combustion');
    if (reactionTypes.singleReplacement) selectedReactionTypes.push('single replacement');
    if (reactionTypes.doubleReplacement) selectedReactionTypes.push('double replacement');

    updateSettings({
      reactionTypes: selectedReactionTypes,
      polyatomicLevel,
      unit,
    });

    navigate('/');
  };

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-2xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">Settings</h1>

        <div className="mb-6 bg-bg-primary p-6 rounded">
          <h2 className="text-xl mb-4 text-text-primary font-sans font-bold">Reaction Types</h2>
          <Checkbox
            label="Synthesis"
            checked={reactionTypes.synthesis}
            onChange={(checked) => setReactionTypes({ ...reactionTypes, synthesis: checked })}
          />
          <Checkbox
            label="Decomposition"
            checked={reactionTypes.decomposition}
            onChange={(checked) => setReactionTypes({ ...reactionTypes, decomposition: checked })}
          />
          <Checkbox
            label="Combustion"
            checked={reactionTypes.combustion}
            onChange={(checked) => setReactionTypes({ ...reactionTypes, combustion: checked })}
          />
          <Checkbox
            label="Single Replacement"
            checked={reactionTypes.singleReplacement}
            onChange={(checked) => setReactionTypes({ ...reactionTypes, singleReplacement: checked })}
          />
          <Checkbox
            label="Double Replacement"
            checked={reactionTypes.doubleReplacement}
            onChange={(checked) => setReactionTypes({ ...reactionTypes, doubleReplacement: checked })}
          />
        </div>

        <div className="mb-6 bg-bg-primary p-6 rounded">
          <h2 className="text-xl mb-4 text-text-primary font-sans font-bold">Polyatomic Ions</h2>
          <RadioButton
            label="All"
            value={2}
            checked={polyatomicLevel === 2}
            onChange={(val) => setPolyatomicLevel(val as number)}
            name="polyatomic"
          />
          <RadioButton
            label="Difficult"
            value={0}
            checked={polyatomicLevel === 0}
            onChange={(val) => setPolyatomicLevel(val as number)}
            name="polyatomic"
          />
          <RadioButton
            label="-Ates and -Ites"
            value={1}
            checked={polyatomicLevel === 1}
            onChange={(val) => setPolyatomicLevel(val as number)}
            name="polyatomic"
          />
        </div>

        <div className="mb-6 bg-bg-primary p-6 rounded">
          <h2 className="text-xl mb-4 text-text-primary font-sans font-bold">Study Unit</h2>
          {[
            { id: 0, name: 'All' },
            { id: 1, name: 'Math Review' },
            { id: 2, name: 'Chemical Nomenclature' },
            { id: 3, name: 'Chemical Quantities' },
            { id: 4, name: 'Chemical Reactions' },
            { id: 5, name: 'Stoichiometry' },
            { id: 6, name: 'Thermochemistry' },
            { id: 7, name: 'Semester One' },
            { id: 8, name: 'Gas Laws' },
            { id: 9, name: 'Electron Configuration' },
            { id: 10, name: 'Periodic Trends and Bonds' },
            { id: 11, name: 'Solutions' },
            { id: 12, name: 'Rates' },
            { id: 13, name: 'Equilibrium' },
            { id: 14, name: 'Thermodynamics' },
            { id: 15, name: 'Acid-Base' },
            { id: 16, name: 'Electrochemistry' },
            { id: 17, name: 'Nuclear Chemistry' },
          ].map((unitOption) => (
            <RadioButton
              key={unitOption.id}
              label={unitOption.name}
              value={unitOption.id}
              checked={unit === unitOption.id}
              onChange={(val) => setUnit(val as number)}
              name="unit"
            />
          ))}
        </div>

        <div className="flex justify-center">
          <Button label="Save Changes" onClick={handleSave} />
        </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
