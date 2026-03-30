import axios from 'axios';
import type {
  QuestionResponse,
  PolyatomicResponse,
  BatchQuestionsRequest,
  BatchQuestionsResponse,
  ModesResponse,
  TableOfContentsResponse,
  PolyatomicChoicesResponse,
} from '../types';

const API_BASE_URL = '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Get all question modes
  getModes: async (): Promise<string[]> => {
    const response = await apiClient.get<ModesResponse>('/modes');
    return response.data.modes;
  },

  // Get table of contents (category groupings)
  getTableOfContents: async () => {
    const response = await apiClient.get<TableOfContentsResponse>('/table-of-contents');
    return response.data.categories;
  },

  // Get a single question by ID
  getQuestion: async (questionId: number, rxType?: string): Promise<QuestionResponse> => {
    const params = rxType ? { rxType } : {};
    const response = await apiClient.get<QuestionResponse>(`/question/${questionId}`, { params });
    return response.data;
  },

  // Get a polyatomic ion question
  getPolyatomicQuestion: async (choices: string[]): Promise<PolyatomicResponse> => {
    const params = { choices: choices.join(',') };
    const response = await apiClient.get<PolyatomicResponse>('/polyatomic', { params });
    return response.data;
  },

  // Get polyatomic choices by difficulty level
  getPolyatomicChoices: async (level: number): Promise<string[]> => {
    const response = await apiClient.get<PolyatomicChoicesResponse>(`/polyatomic-choices/${level}`);
    return response.data.choices;
  },

  // Get batch questions
  getBatchQuestions: async (request: BatchQuestionsRequest) => {
    const response = await apiClient.post<BatchQuestionsResponse>('/questions/batch', request);
    return response.data.questions;
  },

  // Save settings (optional - for future use)
  saveSettings: async (settings: any): Promise<boolean> => {
    const response = await apiClient.post<{ success: boolean }>('/settings', settings);
    return response.data.success;
  },

  // Health check
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await apiClient.get<{ status: string }>('/health');
      return response.data.status === 'ok';
    } catch {
      return false;
    }
  },
};

export default api;
