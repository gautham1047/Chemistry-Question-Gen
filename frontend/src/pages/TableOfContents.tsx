import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { Category } from '../types';
import {
  PageContainer,
  PageHeader,
  Card,
  Badge,
  LoadingState,
  ErrorMessage,
} from '../components';

const TableOfContents = () => {
  const navigate = useNavigate();
  const { setRandomMode } = useAppContext();

  const [categories, setCategories] = useState<Category[]>([]);
  const [modes, setModes] = useState<string[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [cats, modesList] = await Promise.all([
          api.getTableOfContents(),
          api.getModes(),
        ]);
        setCategories(cats.filter((c) => c.name !== 'All' && c.name !== 'Semester One'));
        setModes(modesList);
        setError(null);
      } catch {
        setError('Failed to load curriculum table of contents.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSelectProblem = (id: number) => {
    setRandomMode(false);
    navigate(`/question/${id}`);
  };

  const getProblemTitle = (id: number) => {
    return modes[id - 1] || `Problem #${id}`;
  };

  const filteredCategories = categories
    .map((cat) => ({
      ...cat,
      questionIds: cat.questionIds.filter((qid) => {
        const title = getProblemTitle(qid).toLowerCase();
        return title.includes(search.toLowerCase()) || qid.toString() === search.trim();
      }),
    }))
    .filter((cat) => cat.questionIds.length > 0);

  return (
    <PageContainer wide>
      <PageHeader
        title="Curriculum Index"
        subtitle="Click any problem topic to launch focused practice"
        actions={
          <div className="w-full sm:w-72">
            <input
              type="text"
              placeholder="Filter topics by name or ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-3 py-1.5 bg-slate-800 border border-slate-700 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>
        }
      />

      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {loading ? (
        <LoadingState message="Loading topics..." />
      ) : (
        <div className="space-y-6">
          {filteredCategories.map((cat) => (
            <Card key={cat.id} variant="sm">
              <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-700">
                <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  {cat.name}
                </span>
                <span className="text-xs text-slate-400 font-mono">
                  {cat.questionIds.length} topics
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {cat.questionIds.map((qid) => (
                  <button
                    key={qid}
                    onClick={() => handleSelectProblem(qid)}
                    className="flex items-center gap-2.5 p-2 bg-slate-900/60 hover:bg-slate-700/80 border border-slate-700 text-left transition-colors cursor-pointer group"
                  >
                    <Badge variant="cyan">#{qid}</Badge>
                    <span className="text-xs text-slate-300 group-hover:text-slate-100 truncate">
                      {getProblemTitle(qid)}
                    </span>
                  </button>
                ))}
              </div>
            </Card>
          ))}

          {filteredCategories.length === 0 && (
            <div className="text-center py-12 text-slate-500 text-sm">
              No matching topics found for "{search}".
            </div>
          )}
        </div>
      )}
    </PageContainer>
  );
};

export default TableOfContents;
