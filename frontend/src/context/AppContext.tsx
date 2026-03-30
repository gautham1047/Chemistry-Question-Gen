import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { AppState, AppSettings } from '../types';

interface AppContextType {
  state: AppState;
  updateSettings: (settings: Partial<AppSettings>) => void;
  setLastQuestion: (id: number) => void;
  setAnswer: (answer: string) => void;
  setBatchAnswers: (answers: string[]) => void;
  setRandomMode: (isRandom: boolean) => void;
  setNumQuestions: (num: number) => void;
}

const defaultSettings: AppSettings = {
  reactionTypes: ['synthesis', 'decomposition', 'combustion', 'single replacement', 'double replacement'],
  polyatomicLevel: 2, // All
  unit: 0, // All
  polyatomicChoices: [],
  randomQuestionIds: [],
};

const defaultState: AppState = {
  lastQuestionId: null,
  currentAnswer: '',
  settings: defaultSettings,
  batchAnswers: [],
  isRandomMode: false,
  numQuestions: 10,
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AppState>(defaultState);

  const updateSettings = (newSettings: Partial<AppSettings>) => {
    setState(prev => ({
      ...prev,
      settings: {
        ...prev.settings,
        ...newSettings,
      },
    }));
  };

  const setLastQuestion = (id: number) => {
    setState(prev => ({ ...prev, lastQuestionId: id }));
  };

  const setAnswer = (answer: string) => {
    setState(prev => ({ ...prev, currentAnswer: answer }));
  };

  const setBatchAnswers = (answers: string[]) => {
    setState(prev => ({ ...prev, batchAnswers: answers }));
  };

  const setRandomMode = (isRandom: boolean) => {
    setState(prev => ({ ...prev, isRandomMode: isRandom }));
  };

  const setNumQuestions = (num: number) => {
    setState(prev => ({ ...prev, numQuestions: num }));
  };

  const value: AppContextType = {
    state,
    updateSettings,
    setLastQuestion,
    setAnswer,
    setBatchAnswers,
    setRandomMode,
    setNumQuestions,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
