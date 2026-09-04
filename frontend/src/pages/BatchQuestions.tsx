import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { BatchQuestion } from '../types';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';
import { styles } from '../styles/theme';

const BatchQuestions = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const [questions, setQuestions] = useState<BatchQuestion[]>([]);
  const [revealedIds, setRevealedIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setRevealedIds(new Set());
      const response = await api.getBatchQuestions({
        count: state.numQuestions || 10,
        questionIds: state.settings.randomQuestionIds,
        rxTypes: state.settings.reactionTypes,
      });

      setQuestions(response);
      setError(null);
    } catch {
      setError('Failed to generate batch questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const toggleQuestion = (id: number) => {
    setRevealedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAllAnswers = () => {
    if (revealedIds.size === questions.length) {
      setRevealedIds(new Set());
    } else {
      setRevealedIds(new Set(questions.map((q) => q.id)));
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />

      <main className={`flex-1 ${styles.containerWide}`}>
        <div className="flex items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
          <div>
            <h1 className={styles.heading}>Practice Worksheet</h1>
            <p className={styles.subheading}>
              {questions.length} problems generated
            </p>
          </div>
          <div className="flex items-center gap-2">
            {questions.length > 0 && (
              <Button
                label={revealedIds.size === questions.length ? 'Hide All Answers' : 'Show All Answers'}
                onClick={toggleAllAnswers}
                variant="secondary"
              />
            )}
            <Button
              label="New Worksheet"
              onClick={fetchQuestions}
              variant="primary"
            />
          </div>
        </div>

        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {loading ? (
          <div className={`${styles.card} text-center text-slate-400 py-16`}>
            <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium">Generating your worksheet...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {questions.map((q) => {
              const isRevealed = revealedIds.has(q.id);
              return (
                <div
                  key={q.id}
                  className={`${styles.cardSm} space-y-3`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold bg-slate-700 text-cyan-400 px-2 py-0.5">
                        #{q.id}
                      </span>
                      <span className="text-xs text-slate-400">
                        Topic ID: {q.questionId}
                      </span>
                    </div>
                    <button
                      onClick={() => toggleQuestion(q.id)}
                      className="text-xs text-cyan-400 hover:text-cyan-300 font-medium cursor-pointer transition-colors"
                    >
                      {isRevealed ? '[Hide Answer]' : '[Show Answer]'}
                    </button>
                  </div>

                  <div className="text-slate-100 whitespace-pre-wrap text-base leading-relaxed">
                    {q.question}
                  </div>

                  {isRevealed && (
                    <div className={`${styles.cardEmerald} mt-2`}>
                      <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400 block mb-1">
                        Answer:
                      </span>
                      <div className="text-emerald-100 font-mono text-sm whitespace-pre-wrap">
                        {q.answer}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            <div className="flex items-center justify-between pt-6 border-t border-slate-800">
              <Button label="Return Home" onClick={() => navigate('/')} variant="secondary" />
              <Button label="Generate Another Set" onClick={fetchQuestions} variant="primary" />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default BatchQuestions;
