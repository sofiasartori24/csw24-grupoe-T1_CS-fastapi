import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Resources from './pages/Resources';
import CreateResource from './pages/CreateResource';
import ResourceDetail from './pages/ResourceDetail';
import Menu from './components/Menu';
import './App.css';

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', background: '#f4f6fa' }}>
        <Menu />
        <div style={{ maxWidth: 900, margin: '40px auto', background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px #0001', padding: 32 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/resources/new" element={<CreateResource />} />
            <Route path="/resources/:id" element={<ResourceDetail />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
