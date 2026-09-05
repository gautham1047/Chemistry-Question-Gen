import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { Category } from '../types';
import { PageContainer, Card, Button } from '../components';

const Home = () => {
  const navigate = useNavigate();
  const { setRandomMode, updateSettings } = useAppContext();

  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCatIds, setSelectedCatIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    api.getTableOfContents()
      .then((cats) => {
        setCategories(cats);
        const realIds = cats
          .filter((c) => c.id !== 0 && c.name !== 'Semester One')
          .map((c) => c.id);
        setSelectedCatIds(new Set(realIds));
      })
      .catch(() => {});
  }, []);

  const realCategories = categories.filter(
    (c) => c.id !== 0 && c.name !== 'Semester One' && c.name !== 'All'
  );
  const allCategory = categories.find((c) => c.id === 0 || c.name === 'All');

  const isAllSelected =
    realCategories.length > 0 && realCategories.every((c) => selectedCatIds.has(c.id));

  const toggleAll = () => {
    if (isAllSelected) {
      setSelectedCatIds(new Set());
    } else {
      setSelectedCatIds(new Set(realCategories.map((c) => c.id)));
    }
  };

  const toggleCategory = (id: number) => {
    setSelectedCatIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const getSelectedQuestionIds = (): number[] => {
    if (selectedCatIds.size === 0) {
      return allCategory?.questionIds || Array.from({ length: 73 }, (_, i) => i + 1);
    }
    const ids = new Set<number>();
    realCategories.forEach((cat) => {
      if (selectedCatIds.has(cat.id)) {
        cat.questionIds.forEach((qid) => ids.add(qid));
      }
    });
    return Array.from(ids).sort((a, b) => a - b);
  };

  const activeQuestionCount = getSelectedQuestionIds().length;

  const handleStartPractice = (batch: boolean) => {
    const pool = getSelectedQuestionIds();
    if (pool.length === 0) return;

    updateSettings({ randomQuestionIds: pool });
    if (batch) {
      navigate('/batch-questions');
    } else {
      setRandomMode(true);
      const randomId = pool[Math.floor(Math.random() * pool.length)];
      navigate(`/question/${randomId}`);
    }
  };

  return (
    <PageContainer wide>
      {/* Primary Action Card */}
      <Card className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-700">
          <div>
            <h1 className="text-2xl font-bold text-slate-100 tracking-tight">
              Chemistry Problem Generator
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Select topics below to customize your practice pool, then launch single questions or worksheets.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              label="Start Practice"
              onClick={() => handleStartPractice(false)}
              variant="primary"
              disabled={activeQuestionCount === 0}
            />
            <Button
              label="Start Worksheet"
              onClick={() => handleStartPractice(true)}
              variant="secondary"
              disabled={activeQuestionCount === 0}
            />
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-4 text-xs text-slate-400">
          <div>
            Active Pool: <span className="text-cyan-400 font-mono font-semibold">{activeQuestionCount}</span> topics selected across{' '}
            <span className="text-cyan-400 font-mono font-semibold">{selectedCatIds.size}</span> categories
          </div>
          <div className="flex items-center gap-2">
            <Button label="Polyatomic Ion Drill" onClick={() => navigate('/polyatomic')} variant="secondary" size="sm" />
            <Button label="Curriculum Index" onClick={() => navigate('/table-of-contents')} variant="secondary" size="sm" />
          </div>
        </div>
      </Card>

      {/* Topic Multi-Select Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
              Topic Selection
            </h2>
            <span className="text-xs text-slate-500">
              (Click cards to toggle inclusion)
            </span>
          </div>

          <Button
            label={isAllSelected ? 'Deselect All' : 'Select All Categories'}
            onClick={toggleAll}
            variant="outline"
            size="sm"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {/* Master All Card */}
          <Card
            variant="interactive"
            selected={isAllSelected}
            onClick={toggleAll}
            className="flex flex-col justify-between"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                All Topics
              </span>
              <span className={`w-4 h-4 border flex items-center justify-center text-xs font-mono font-bold ${
                isAllSelected ? 'border-cyan-400 bg-cyan-600 text-white' : 'border-slate-600 bg-slate-800'
              }`}>
                {isAllSelected ? 'X' : ''}
              </span>
            </div>
            <div className="text-xs text-slate-400">
              Toggle all {realCategories.length} categories simultaneously
            </div>
          </Card>

          {/* Individual Category Cards */}
          {realCategories.map((cat) => {
            const isChecked = selectedCatIds.has(cat.id);
            return (
              <Card
                key={cat.id}
                variant="interactive"
                selected={isChecked}
                onClick={() => toggleCategory(cat.id)}
                className="flex flex-col justify-between"
              >
                <div className="flex items-start justify-between gap-2 mb-3">
                  <span className={`text-sm font-medium ${isChecked ? 'text-slate-100' : 'text-slate-400'}`}>
                    {cat.name}
                  </span>
                  <span className={`w-4 h-4 border flex items-center justify-center text-xs font-mono font-bold flex-shrink-0 ${
                    isChecked ? 'border-cyan-400 bg-cyan-600 text-white' : 'border-slate-600 bg-slate-800'
                  }`}>
                    {isChecked ? 'X' : ''}
                  </span>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-700/50">
                  <span>Category #{cat.id}</span>
                  <span className="font-mono">{cat.questionIds.length} types</span>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </PageContainer>
  );
};

export default Home;
