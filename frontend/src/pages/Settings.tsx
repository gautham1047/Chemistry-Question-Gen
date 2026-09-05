import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { Category } from '../types';
import {
  PageContainer,
  PageHeader,
  Card,
  Button,
  Checkbox,
  RadioButton,
} from '../components';

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

  const sectionTitleClass = 'text-xs font-semibold uppercase tracking-wider text-cyan-400 mb-3';

  return (
    <PageContainer>
      <PageHeader
        title="Settings"
        subtitle="Customize problem generation parameters"
        actions={
          <>
            {saved && <span className="text-xs text-emerald-400 font-mono font-medium">[Saved]</span>}
            <Button label="Save Changes" onClick={handleSave} variant="primary" />
          </>
        }
      />

      <div className="space-y-4">
        {/* Reaction Types */}
        <Card variant="sm">
          <h2 className={sectionTitleClass}>Reaction Types (for equation problems)</h2>
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
        </Card>

        {/* Polyatomic Ion Scope */}
        <Card variant="sm">
          <h2 className={sectionTitleClass}>Polyatomic Ion Set</h2>
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
        </Card>

        {/* Batch Test Count */}
        <Card variant="sm">
          <h2 className={sectionTitleClass}>Test Worksheet Size</h2>
          <div className="flex items-center gap-2">
            {[5, 10, 15, 20].map((cnt) => (
              <Button
                key={cnt}
                label={`${cnt} Questions`}
                onClick={() => setBatchCount(cnt)}
                variant={batchCount === cnt ? 'primary' : 'secondary'}
                size="sm"
              />
            ))}
          </div>
        </Card>

        {/* Target Study Unit */}
        <Card variant="sm">
          <h2 className={sectionTitleClass}>Default Study Unit Filter</h2>
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
        </Card>

        <div className="flex items-center justify-between pt-4 border-t border-slate-800">
          <Button label="Return to Practice" onClick={() => navigate('/')} variant="secondary" />
          <Button label="Save & Apply" onClick={handleSave} variant="primary" />
        </div>
      </div>
    </PageContainer>
  );
};

export default Settings;
