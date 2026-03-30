import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { Header } from '../components/Header';
import Button from '../components/Button';

const BatchAnswers = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const handleReturnHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">Answers:</h1>

          <div className="mb-6 text-text-primary font-sans">
            {state.batchAnswers.map((answer, idx) => (
              <div key={idx} className="mb-4">
                {answer}
              </div>
            ))}
          </div>

          <div className="flex justify-center">
            <Button label="Return Home?" onClick={handleReturnHome} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatchAnswers;
