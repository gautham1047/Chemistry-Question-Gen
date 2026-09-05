import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import {
  PageContainer,
  Card,
  Button,
  Badge,
  LoadingState,
  AnswerBox,
  ErrorMessage,
} from '../components';

const Polyatomic = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIonQuestion = async () => {
    try {
      setLoading(true);
      setShowAnswer(false);
      const choices = state.settings.polyatomicChoices.length > 0
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

  const levelLabel =
    state.settings.polyatomicLevel === 0
      ? 'Difficult'
      : state.settings.polyatomicLevel === 1
      ? '-Ates & -Ites'
      : 'All';

  return (
    <PageContainer centered>
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {loading ? (
        <LoadingState message="Fetching ion question..." />
      ) : (
        <div className="space-y-4">
          <Card>
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-700">
              <Badge variant="cyan">Polyatomic Ion Drill</Badge>
              <Badge variant="slate">Level: {levelLabel}</Badge>
            </div>

            <div className="text-slate-100 text-lg leading-relaxed mb-6 font-medium">
              {question}
            </div>

            {!showAnswer && (
              <div className="flex items-center gap-3">
                <Button label="Reveal Answer" onClick={() => setShowAnswer(true)} variant="primary" />
                <Button label="Skip to Next Ion" onClick={fetchIonQuestion} variant="secondary" />
              </div>
            )}
          </Card>

          {showAnswer && (
            <AnswerBox
              answer={answer}
              large
              actions={
                <>
                  <Button label="Next Ion" onClick={fetchIonQuestion} variant="accent" />
                  <Button label="Configure Ions" onClick={() => navigate('/settings')} variant="secondary" />
                  <Button label="Home" onClick={() => navigate('/')} variant="secondary" />
                </>
              }
            />
          )}
        </div>
      )}
    </PageContainer>
  );
};

export default Polyatomic;
