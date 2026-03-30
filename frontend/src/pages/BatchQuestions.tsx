import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';

const BatchQuestions = () => {
  const navigate = useNavigate();
  const { setBatchAnswers, state } = useAppContext();
  const [questions, setQuestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        const response = await api.getBatchQuestions({
          count: state.numQuestions,
          questionIds: state.settings.randomQuestionIds,
          rxTypes: state.settings.reactionTypes,
        });

        const questionTexts = response.map(
          (q) => `${q.id}. ${q.question}`
        );
        const answerTexts = response.map(
          (q) => `${q.id}. ${q.answer}`
        );

        setQuestions(questionTexts);
        setBatchAnswers(answerTexts);
        setError(null);
      } catch (err) {
        setError('Failed to load questions. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  const handleGetAnswers = () => {
    navigate('/batch-answers');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary">
        <Header />
        <div className="flex items-center justify-center pt-20">
          <div className="text-2xl text-text-primary">Loading questions...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">Questions:</h1>

          {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

          <div className="mb-6 text-text-primary font-sans">
            {questions.map((q, idx) => (
              <div key={idx} className="mb-4 whitespace-pre-wrap">
                {q}
              </div>
            ))}
          </div>

          <div className="flex justify-center">
            <Button label="Get Answers?" onClick={handleGetAnswers} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatchQuestions;
