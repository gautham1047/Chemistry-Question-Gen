import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { Category } from '../types';
import { Header } from '../components/Header';
import ErrorMessage from '../components/ErrorMessage';
import { styles } from '../styles/theme';

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
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />

      <main className={`flex-1 ${styles.containerWide}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
          <div>
            <h1 className={styles.heading}>Curriculum Index</h1>
            <p className={styles.subheading}>
              Click any problem topic to launch focused practice
            </p>
          </div>
          <div className="w-full sm:w-72">
            <input
              type="text"
              placeholder="Filter topics by name or ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className={styles.input}
            />
          </div>
        </div>

        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {loading ? (
          <div className={`${styles.card} text-center text-slate-400 py-16`}>
            <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium">Loading topics...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {filteredCategories.map((cat) => (
              <div key={cat.id} className={styles.cardSm}>
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-700">
                  <span className={styles.sectionTitle}>{cat.name}</span>
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
                      <span className="font-mono text-xs text-cyan-400 bg-cyan-950/70 border border-cyan-800/40 px-1.5 py-0.5 flex-shrink-0">
                        #{qid}
                      </span>
                      <span className="text-xs text-slate-300 group-hover:text-slate-100 truncate">
                        {getProblemTitle(qid)}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            ))}

            {filteredCategories.length === 0 && (
              <div className="text-center py-12 text-slate-500 text-sm">
                No matching topics found for "{search}".
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default TableOfContents;
