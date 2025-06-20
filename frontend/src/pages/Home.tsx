import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div style={{ textAlign: 'center', marginTop: '3rem' }}>
            <h1>Bem-vindo ao Sistema de Gerenciamento de Recursos</h1>
            <p>Este sistema permite visualizar e gerenciar recursos da universidade de forma simples e eficiente.</p>
            <Link to="/resources" style={{
                display: 'inline-block',
                marginTop: '2rem',
                padding: '0.75rem 2rem',
                background: '#1976d2',
                color: '#fff',
                borderRadius: '5px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1.1rem'
            }}>
                Ver Recursos
            </Link>
        </div>
    );
}
