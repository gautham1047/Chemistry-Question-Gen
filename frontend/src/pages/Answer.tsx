import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { Header } from '../components/Header';
import Button from '../components/Button';

const Answer = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const handleGetAnother = () => {
    if (state.lastQuestionId) {
      navigate(`/question/${state.lastQuestionId}`);
    }
  };

  const handleBackHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-3xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">
            Answer: {state.currentAnswer}
          </h1>

          <div className="flex gap-4 justify-center">
            <Button label="Get Another?" onClick={handleGetAnother} />
            <Button label="Back to home" onClick={handleBackHome} variant="secondary" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Answer;
