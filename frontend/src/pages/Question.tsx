import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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

const Question = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { state, setLastQuestion } = useAppContext();

  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestionData = async (questionId: number) => {
    try {
      setLoading(true);
      setShowAnswer(false);
      setLastQuestion(questionId);

      const rxType = state.settings.reactionTypes.length > 0
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
    const num = parseInt(id || '', 10);
    if (!isNaN(num)) fetchQuestionData(num);
  }, [id]);

  const handleNextQuestion = () => {
    const currentId = parseInt(id || '1', 10);

    if (state.isRandomMode) {
      const pool = state.settings.randomQuestionIds.length > 0
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
    <PageContainer centered>
      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {loading ? (
        <LoadingState message="Generating problem..." />
      ) : (
        <div className="space-y-4">
          <Card>
            <div className="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-slate-700">
              <Badge variant="cyan">Problem #{id}</Badge>
              {state.isRandomMode && <Badge variant="slate">Random Mode</Badge>}
            </div>

            <div className="text-slate-100 text-lg leading-relaxed whitespace-pre-wrap mb-6">
              {question}
            </div>

            {!showAnswer && (
              <div className="flex items-center gap-3">
                <Button label="Reveal Answer" onClick={() => setShowAnswer(true)} variant="primary" />
                <Button label="Reroll Question" onClick={handleRepeatSameType} variant="secondary" />
              </div>
            )}
          </Card>

          {showAnswer && (
            <AnswerBox
              answer={answer}
              actions={
                <>
                  <Button
                    label={state.isRandomMode ? 'Next Random Question' : 'Another of This Type'}
                    onClick={handleNextQuestion}
                    variant="accent"
                  />
                  {state.isRandomMode && (
                    <Button label="Another of This Type" onClick={handleRepeatSameType} variant="secondary" />
                  )}
                  <Button label="All Topics" onClick={() => navigate('/table-of-contents')} variant="secondary" />
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

export default Question;
