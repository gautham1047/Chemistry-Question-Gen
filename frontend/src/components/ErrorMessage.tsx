import React from 'react';

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss }) => {
  return (
    <div className="bg-red-950/50 border border-red-800 text-red-300 px-4 py-2.5 text-sm mb-4 flex items-center justify-between" role="alert">
      <span>{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-red-400 hover:text-red-200 ml-4 font-bold text-lg leading-none cursor-pointer"
        >
          &times;
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
