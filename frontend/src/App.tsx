import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import Home from './pages/Home';
import Question from './pages/Question';
import Settings from './pages/Settings';
import Polyatomic from './pages/Polyatomic';
import BatchQuestions from './pages/BatchQuestions';
import TableOfContents from './pages/TableOfContents';

const App: React.FC = () => {
  return (
    <AppProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/question/:id" element={<Question />} />
          <Route path="/polyatomic" element={<Polyatomic />} />
          <Route path="/batch-questions" element={<BatchQuestions />} />
          <Route path="/table-of-contents" element={<TableOfContents />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AppProvider>
  );
};

export default App;
