import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';

const Question = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { setAnswer, state } = useAppContext();
  const [question, setQuestion] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestion = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const rxType = state.settings.reactionTypes.length > 0
          ? state.settings.reactionTypes[Math.floor(Math.random() * state.settings.reactionTypes.length)]
          : undefined;

        const response = await api.getQuestion(parseInt(id), rxType);
        setQuestion(response.question);
        setAnswer(response.answer);
        setError(null);
      } catch (err) {
        setError('Failed to load question. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestion();
  }, [id]);

  const handleGetAnswer = () => {
    navigate('/answer');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary">
        <Header />
        <div className="flex items-center justify-center pt-20">
          <div className="text-2xl text-text-primary">Loading question...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-3xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">Question:</h1>

          {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

          <div className="mb-6 whitespace-pre-wrap text-text-primary font-sans text-lg">
            {question}
          </div>

          <div className="flex justify-center">
            <Button label="Get Answer?" onClick={handleGetAnswer} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Question;
