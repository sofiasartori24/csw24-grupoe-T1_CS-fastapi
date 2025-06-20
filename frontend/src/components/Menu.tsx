import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const menuStyle: React.CSSProperties = {
  background: '#1976d2',
  padding: '0.5rem 0',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '2rem',
  boxShadow: '0 2px 8px #0002',
  position: 'sticky',
  top: 0,
  zIndex: 100,
};

const linkStyle: React.CSSProperties = {
  color: '#fff',
  textDecoration: 'none',
  fontWeight: 600,
  fontSize: '1.1rem',
  padding: '0.5rem 1.2rem',
  borderRadius: 6,
  transition: 'background 0.2s',
};

const activeStyle: React.CSSProperties = {
  background: '#1565c0',
};

const Menu: React.FC = () => {
  const location = useLocation();
  return (
    <nav style={menuStyle}>
      <Link to="/" style={{ ...linkStyle, ...(location.pathname === '/' ? activeStyle : {}) }}>Início</Link>
      <Link to="/resources" style={{ ...linkStyle, ...(location.pathname.startsWith('/resources') && location.pathname !== '/resources/new' && !location.pathname.match(/^\/resources\/\d+$/) ? activeStyle : {}) }}>Recursos</Link>
      <Link to="/resources/new" style={{ ...linkStyle, ...(location.pathname === '/resources/new' ? activeStyle : {}) }}>Novo Recurso</Link>
    </nav>
  );
};

export default Menu;
