export interface QuestionResponse {
  question: string;
  answer: string;
  questionId: number;
}

export interface PolyatomicResponse {
  question: string;
  answer: string;
}

export interface BatchQuestionsRequest {
  count: number;
  questionIds?: number[];
  rxTypes: string[];
}

export interface BatchQuestion {
  id: number;
  questionId: number;
  question: string;
  answer: string;
}

export interface Category {
  id: number;
  name: string;
  questionIds: number[];
}

export interface AppSettings {
  reactionTypes: string[];
  polyatomicLevel: number;
  unit: number;
  polyatomicChoices: string[];
  randomQuestionIds: number[];
}

export interface AppState {
  lastQuestionId: number | null;
  currentAnswer: string;
  settings: AppSettings;
  batchAnswers: string[];
  isRandomMode: boolean;
  numQuestions: number;
}

export type ReactionType =
  | 'synthesis'
  | 'decomposition'
  | 'combustion'
  | 'single replacement'
  | 'double replacement';

export interface ModesResponse {
  modes: string[];
}

export interface TableOfContentsResponse {
  categories: Category[];
}

export interface PolyatomicChoicesResponse {
  choices: string[];
}

export interface BatchQuestionsResponse {
  questions: BatchQuestion[];
}
