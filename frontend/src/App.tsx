import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Resources from './pages/Resources';
import CreateResource from './pages/CreateResource';
import ResourceDetail from './pages/ResourceDetail';
import Admin from './pages/Admin';
import Coordenador from './pages/Coordenador';
import Menu from './components/Menu';

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', background: '#f4f6fa' }}>
        <Menu />
        <div style={{ maxWidth: 900, margin: '40px auto', background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px #0001', padding: 32 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/admin" element={<Admin />} />    
            <Route path="/coordinator" element={<Coordenador />} />
    
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
