import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/apiClient';
import { Header } from '../components/Header';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';

const TableOfContents = () => {
  const navigate = useNavigate();
  const [modes, setModes] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchModes = async () => {
      try {
        setLoading(true);
        const modesData = await api.getModes();
        setModes(modesData);
        setError(null);
      } catch (err) {
        setError('Failed to load table of contents. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchModes();
  }, []);

  const handleGoHome = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary">
        <Header />
        <div className="flex items-center justify-center pt-20">
          <div className="text-2xl text-text-primary">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg-primary">
      <Header />
      <div className="flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl w-full bg-highlight p-8 rounded">
          <h1 className="text-3xl mb-6 text-text-primary font-sans">Options:</h1>

          {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

          <div className="mb-6 text-text-primary font-sans">
            {modes.map((mode, idx) => (
              <div key={idx} className="mb-2">
                {idx + 1}. {mode}
              </div>
            ))}
          </div>

          <div className="flex justify-center">
            <Button label="Go Home?" onClick={handleGoHome} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TableOfContents;
