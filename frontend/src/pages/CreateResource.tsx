import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const CreateResource: React.FC = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await api.post('/resources', { name, description });
            navigate('/resources');
        } catch (err: any) {
            setError('Erro ao cadastrar recurso.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: 500, margin: '2rem auto' }}>
            <h2>Cadastrar Novo Recurso</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 16 }}>
                    <label>Nome:</label>
                    <input
                        type="text"
                        value={name}
                        onChange={e => setName(e.target.value)}
                        required
                        style={{ width: '100%', padding: 8 }}
                    />
                </div>
                <div style={{ marginBottom: 16 }}>
                    <label>Descrição:</label>
                    <textarea
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        required
                        style={{ width: '100%', padding: 8 }}
                    />
                </div>
                {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
                <button type="submit" disabled={loading} style={{ padding: '8px 24px' }}>
                    {loading ? 'Salvando...' : 'Cadastrar'}
                </button>
            </form>
        </div>
    );
};

export default CreateResource;
