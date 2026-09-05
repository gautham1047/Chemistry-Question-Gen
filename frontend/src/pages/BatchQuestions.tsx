import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import api from '../api/apiClient';
import type { BatchQuestion } from '../types';
import {
  PageContainer,
  PageHeader,
  Card,
  Button,
  Badge,
  LoadingState,
  AnswerBox,
  ErrorMessage,
} from '../components';

const BatchQuestions = () => {
  const navigate = useNavigate();
  const { state } = useAppContext();

  const [questions, setQuestions] = useState<BatchQuestion[]>([]);
  const [revealedIds, setRevealedIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setRevealedIds(new Set());
      const response = await api.getBatchQuestions({
        count: state.numQuestions || 10,
        questionIds: state.settings.randomQuestionIds,
        rxTypes: state.settings.reactionTypes,
      });
      setQuestions(response);
      setError(null);
    } catch {
      setError('Failed to generate batch questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const toggleQuestion = (id: number) => {
    setRevealedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleAllAnswers = () => {
    if (revealedIds.size === questions.length) {
      setRevealedIds(new Set());
    } else {
      setRevealedIds(new Set(questions.map((q) => q.id)));
    }
  };

  const isAllRevealed = questions.length > 0 && revealedIds.size === questions.length;

  return (
    <PageContainer wide>
      <PageHeader
        title="Practice Worksheet"
        subtitle={`${questions.length} problems generated`}
        actions={
          <>
            {questions.length > 0 && (
              <Button
                label={isAllRevealed ? 'Hide All Answers' : 'Show All Answers'}
                onClick={toggleAllAnswers}
                variant="secondary"
              />
            )}
            <Button label="New Worksheet" onClick={fetchQuestions} variant="primary" />
          </>
        }
      />

      {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

      {loading ? (
        <LoadingState message="Generating your worksheet..." />
      ) : (
        <div className="space-y-4">
          {questions.map((q) => {
            const isRevealed = revealedIds.has(q.id);
            return (
              <Card key={q.id} variant="sm" className="space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="cyan">#{q.id}</Badge>
                    <span className="text-xs text-slate-400">Topic ID: {q.questionId}</span>
                  </div>
                  <Button
                    label={isRevealed ? '[Hide Answer]' : '[Show Answer]'}
                    onClick={() => toggleQuestion(q.id)}
                    variant="ghost"
                    size="sm"
                  />
                </div>

                <div className="text-slate-100 whitespace-pre-wrap text-base leading-relaxed">
                  {q.question}
                </div>

                {isRevealed && <AnswerBox answer={q.answer} />}
              </Card>
            );
          })}

          <div className="flex items-center justify-between pt-6 border-t border-slate-800">
            <Button label="Return Home" onClick={() => navigate('/')} variant="secondary" />
            <Button label="Generate Another Set" onClick={fetchQuestions} variant="primary" />
          </div>
        </div>
      )}
    </PageContainer>
  );
};

export default BatchQuestions;
