import React, { type ReactNode } from 'react';
import { Card } from './Card';

interface AnswerBoxProps {
  answer: string;
  title?: string;
  large?: boolean;
  actions?: ReactNode;
  className?: string;
}

export const AnswerBox: React.FC<AnswerBoxProps> = ({
  answer,
  title = 'Answer',
  large = false,
  actions,
  className = '',
}) => {
  return (
    <Card variant="emerald" className={`space-y-4 ${className}`}>
      <div>
        <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1.5">
          {title}
        </h3>
        <p className={`text-emerald-100 font-mono whitespace-pre-wrap ${large ? 'text-2xl font-semibold' : 'text-lg'}`}>
          {answer}
        </p>
      </div>

      {actions && (
        <div className="pt-3 border-t border-emerald-900/50 flex flex-wrap items-center gap-2.5">
          {actions}
        </div>
      )}
    </Card>
  );
};

export default AnswerBox;
