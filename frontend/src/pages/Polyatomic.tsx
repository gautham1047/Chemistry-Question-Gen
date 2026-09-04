import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';
import { styles } from '../styles/theme';

const Polyatomic = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const [question, setQuestion] = useState<string>('');
  const [answer, setAnswer] = useState<string>('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIonQuestion = async () => {
    try {
      setLoading(true);
      setShowAnswer(false);
      const choices =
        state.settings.polyatomicChoices.length > 0
          ? state.settings.polyatomicChoices
          : await api.getPolyatomicChoices(state.settings.polyatomicLevel ?? 2);

      const response = await api.getPolyatomicQuestion(choices);
      setQuestion(response.question);
      setAnswer(response.answer);
      setError(null);
    } catch {
      setError('Failed to load polyatomic ion question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIonQuestion();
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      <Header />

      <main className={`flex-1 ${styles.container} flex flex-col justify-center`}>
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {loading ? (
          <div className={`${styles.card} text-center text-slate-400 py-16`}>
            <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium">Fetching ion question...</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className={styles.card}>
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-700">
                <span className={styles.badgeCyan}>
                  Polyatomic Ion Drill
                </span>
                <span className={styles.badgeSlate}>
                  Level: {state.settings.polyatomicLevel === 0 ? 'Difficult' : state.settings.polyatomicLevel === 1 ? '-Ates & -Ites' : 'All'}
                </span>
              </div>

              <div className="text-slate-100 text-lg leading-relaxed mb-6 font-medium">
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
                    label="Skip to Next Ion"
                    onClick={fetchIonQuestion}
                    variant="secondary"
                  />
                </div>
              )}
            </div>

            {showAnswer && (
              <div className={`${styles.cardEmerald} space-y-4`}>
                <div>
                  <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1.5">
                    Answer
                  </h3>
                  <p className="text-emerald-100 text-2xl font-mono font-semibold">
                    {answer}
                  </p>
                </div>

                <div className="pt-3 border-t border-emerald-900/50 flex flex-wrap items-center gap-2.5">
                  <Button
                    label="Next Ion"
                    onClick={fetchIonQuestion}
                    variant="accent"
                  />
                  <Button
                    label="Configure Ions"
                    onClick={() => navigate('/settings')}
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

export default Polyatomic;
