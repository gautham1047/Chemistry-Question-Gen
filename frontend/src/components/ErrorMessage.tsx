import React from 'react';

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss }) => {
  return (
    <div className="bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <span className="block sm:inline">{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="absolute top-0 bottom-0 right-0 px-4 py-3"
        >
          <span className="text-2xl">&times;</span>
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
