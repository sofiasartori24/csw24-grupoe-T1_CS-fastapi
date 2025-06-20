import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Resources from './pages/Resources';
import CreateResource from './pages/CreateResource';
import ResourceDetail from './pages/ResourceDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/resources/new" element={<CreateResource />} />
        <Route path="/resources/:id" element={<ResourceDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
