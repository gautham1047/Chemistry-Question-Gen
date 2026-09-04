import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';
import { styles } from '../styles/theme';

const Question = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { state, setLastQuestion } = useAppContext();

  const [question, setQuestion] = useState<string>('');
  const [answer, setAnswer] = useState<string>('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestionData = async (questionId: number) => {
    try {
      setLoading(true);
      setShowAnswer(false);
      setLastQuestion(questionId);

      const rxType =
        state.settings.reactionTypes.length > 0
          ? state.settings.reactionTypes[Math.floor(Math.random() * state.settings.reactionTypes.length)]
          : undefined;

      const response = await api.getQuestion(questionId, rxType);
      setQuestion(response.question);
      setAnswer(response.answer);
      setError(null);
    } catch {
      setError('Failed to generate problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!id) return;
    const num = parseInt(id, 10);
    if (!isNaN(num)) {
      fetchQuestionData(num);
    }
  }, [id]);

  const handleNextQuestion = () => {
    const currentId = parseInt(id || '1', 10);

    if (state.isRandomMode) {
      const pool =
        state.settings.randomQuestionIds.length > 0
          ? state.settings.randomQuestionIds
          : Array.from({ length: 73 }, (_, i) => i + 1);
      const nextId = pool[Math.floor(Math.random() * pool.length)];

      if (nextId === currentId) {
        fetchQuestionData(currentId);
      } else {
        navigate(`/question/${nextId}`);
      }
    } else {
      fetchQuestionData(currentId);
    }
  };

  const handleRepeatSameType = () => {
    const currentId = parseInt(id || '1', 10);
    fetchQuestionData(currentId);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />

      <main className={`flex-1 ${styles.container} flex flex-col justify-center`}>
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {loading ? (
          <div className={`${styles.card} text-center text-slate-400 py-16`}>
            <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium">Generating problem...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Question Card */}
            <div className={styles.card}>
              <div className="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-slate-700">
                <span className={styles.badgeCyan}>
                  Problem #{id}
                </span>
                {state.isRandomMode && (
                  <span className={styles.badgeSlate}>
                    Random Mode
                  </span>
                )}
              </div>

              <div className="text-slate-100 text-lg leading-relaxed whitespace-pre-wrap mb-6">
                {question}
              </div>

              {!showAnswer && (
                <div className="flex items-center gap-3">
                  <Button
                    label="Reveal Answer"
                    onClick={() => setShowAnswer(true)}
                    variant="primary"
                  />
                  <Button
                    label="Reroll Question"
                    onClick={handleRepeatSameType}
                    variant="secondary"
                  />
                </div>
              )}
            </div>

            {/* Answer revealed directly underneath */}
            {showAnswer && (
              <div className={`${styles.cardEmerald} space-y-4`}>
                <div>
                  <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1.5">
                    Answer
                  </h3>
                  <p className="text-emerald-100 text-lg whitespace-pre-wrap font-mono">
                    {answer}
                  </p>
                </div>

                {/* Options on what to do next */}
                <div className="pt-3 border-t border-emerald-900/50 flex flex-wrap items-center gap-2.5">
                  <Button
                    label={state.isRandomMode ? 'Next Random Question' : 'Another of This Type'}
                    onClick={handleNextQuestion}
                    variant="accent"
                  />
                  {state.isRandomMode && (
                    <Button
                      label="Another of This Type"
                      onClick={handleRepeatSameType}
                      variant="secondary"
                    />
                  )}
                  <Button
                    label="All Topics"
                    onClick={() => navigate('/table-of-contents')}
                    variant="secondary"
                  />
                  <Button
                    label="Home"
                    onClick={() => navigate('/')}
                    variant="secondary"
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default Question;
