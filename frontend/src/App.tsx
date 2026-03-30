import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import Home from './pages/Home';
import Question from './pages/Question';
import Answer from './pages/Answer';
import Settings from './pages/Settings';
import Polyatomic from './pages/Polyatomic';
import PolyatomicAnswer from './pages/PolyatomicAnswer';
import BatchQuestions from './pages/BatchQuestions';
import BatchAnswers from './pages/BatchAnswers';
import TableOfContents from './pages/TableOfContents';
import Error from './pages/Error';

const App: React.FC = () => {
  return (
    <AppProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/question/:id" element={<Question />} />
          <Route path="/answer" element={<Answer />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/polyatomic" element={<Polyatomic />} />
          <Route path="/polyatomic-answer" element={<PolyatomicAnswer />} />
          <Route path="/batch-questions" element={<BatchQuestions />} />
          <Route path="/batch-answers" element={<BatchAnswers />} />
          <Route path="/table-of-contents" element={<TableOfContents />} />
          <Route path="/error" element={<Error />} />
        </Routes>
      </Router>
    </AppProvider>
  );
};

export default App;
