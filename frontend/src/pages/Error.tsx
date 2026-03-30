import { useNavigate, useLocation } from 'react-router-dom';
import { Header } from '../components/Header';
import Button from '../components/Button';

const Error = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const errorType = location.state?.errorType || 'unknown';

  const errorMessages: Record<string, string> = {
    'invalid-input': 'You can only input positive integers!',
    'empty-input': 'You cannot input an empty textbox!',
    'unknown': 'An error occurred. Please try again.',
  };

  const errorMessage = errorMessages[errorType] || errorMessages['unknown'];

  const handleReturnHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-2xl w-full bg-bg-secondary border-2 border-text-secondary p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">{errorMessage}</h1>

          <div className="flex justify-center">
            <Button label="Return Home" onClick={handleReturnHome} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Error;
