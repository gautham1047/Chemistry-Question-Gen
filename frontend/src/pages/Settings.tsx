import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { Category } from '../types';
import { Header } from '../components/Header';
import Button from '../components/Button';
import Checkbox from '../components/Checkbox';
import RadioButton from '../components/RadioButton';
import { styles } from '../styles/theme';

const Settings = () => {
  const navigate = useNavigate();
  const { state, updateSettings, setNumQuestions } = useAppContext();

  const [categories, setCategories] = useState<Category[]>([]);
  const [reactionTypes, setReactionTypes] = useState({
    synthesis: state.settings.reactionTypes.includes('synthesis'),
    decomposition: state.settings.reactionTypes.includes('decomposition'),
    combustion: state.settings.reactionTypes.includes('combustion'),
    singleReplacement: state.settings.reactionTypes.includes('single replacement'),
    doubleReplacement: state.settings.reactionTypes.includes('double replacement'),
  });

  const [polyatomicLevel, setPolyatomicLevel] = useState(state.settings.polyatomicLevel ?? 2);
  const [selectedUnit, setSelectedUnit] = useState<number>(state.settings.unit ?? 0);
  const [batchCount, setBatchCount] = useState<number>(state.numQuestions || 10);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.getTableOfContents().then((cats) => setCategories(cats)).catch(() => {});
  }, []);

  const handleSave = async () => {
    const selectedReactionTypes: string[] = [];
    if (reactionTypes.synthesis) selectedReactionTypes.push('synthesis');
    if (reactionTypes.decomposition) selectedReactionTypes.push('decomposition');
    if (reactionTypes.combustion) selectedReactionTypes.push('combustion');
    if (reactionTypes.singleReplacement) selectedReactionTypes.push('single replacement');
    if (reactionTypes.doubleReplacement) selectedReactionTypes.push('double replacement');

    const matchedCat = categories.find((c) => c.id === selectedUnit);
    const randomQuestionIds = matchedCat ? matchedCat.questionIds : [];

    let polyChoices = state.settings.polyatomicChoices;
    try {
      polyChoices = await api.getPolyatomicChoices(polyatomicLevel);
    } catch {}

    updateSettings({
      reactionTypes: selectedReactionTypes,
      polyatomicLevel,
      unit: selectedUnit,
      randomQuestionIds,
      polyatomicChoices: polyChoices,
    });
    setNumQuestions(batchCount);

    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />

      <main className={`flex-1 ${styles.container}`}>
        <div className="flex items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
          <div>
            <h1 className={styles.heading}>Settings</h1>
            <p className={styles.subheading}>Customize problem generation parameters</p>
          </div>
          <div className="flex items-center gap-3">
            {saved && <span className="text-xs text-emerald-400 font-mono font-medium">[Saved]</span>}
            <Button label="Save Changes" onClick={handleSave} variant="primary" />
          </div>
        </div>

        <div className="space-y-4">
          {/* Reaction Types */}
          <div className={styles.cardSm}>
            <h2 className={`${styles.sectionTitle} mb-3`}>
              Reaction Types (for equation problems)
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-1">
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
          </div>

          {/* Polyatomic Ion Scope */}
          <div className={styles.cardSm}>
            <h2 className={`${styles.sectionTitle} mb-3`}>
              Polyatomic Ion Set
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <RadioButton
                label="All (46 ions)"
                value={2}
                checked={polyatomicLevel === 2}
                onChange={(val) => setPolyatomicLevel(val as number)}
                name="polyatomic"
              />
              <RadioButton
                label="-Ates & -Ites (38 ions)"
                value={1}
                checked={polyatomicLevel === 1}
                onChange={(val) => setPolyatomicLevel(val as number)}
                name="polyatomic"
              />
              <RadioButton
                label="Difficult (13 ions)"
                value={0}
                checked={polyatomicLevel === 0}
                onChange={(val) => setPolyatomicLevel(val as number)}
                name="polyatomic"
              />
            </div>
          </div>

          {/* Batch Test Count */}
          <div className={styles.cardSm}>
            <h2 className={`${styles.sectionTitle} mb-3`}>
              Test Worksheet Size
            </h2>
            <div className="flex items-center gap-3">
              {[5, 10, 15, 20].map((cnt) => (
                <button
                  key={cnt}
                  type="button"
                  onClick={() => setBatchCount(cnt)}
                  className={`px-3 py-1.5 text-xs font-semibold cursor-pointer transition-colors ${
                    batchCount === cnt
                      ? 'bg-cyan-600 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {cnt} Questions
                </button>
              ))}
            </div>
          </div>

          {/* Target Study Unit */}
          <div className={styles.cardSm}>
            <h2 className={`${styles.sectionTitle} mb-3`}>
              Default Study Unit Filter
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 max-h-64 overflow-y-auto pr-2">
              {categories.map((cat) => (
                <RadioButton
                  key={cat.id}
                  label={`${cat.name} (${cat.questionIds.length})`}
                  value={cat.id}
                  checked={selectedUnit === cat.id}
                  onChange={(val) => setSelectedUnit(val as number)}
                  name="unit"
                />
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <Button label="Return to Practice" onClick={() => navigate('/')} variant="secondary" />
            <Button label="Save & Apply" onClick={handleSave} variant="primary" />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Settings;
