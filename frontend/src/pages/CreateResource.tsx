import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const CreateResource: React.FC = () => {
    const [description, setDescription] = useState('');
    const [status, setStatus] = useState('available');
    const [resourceTypeId, setResourceTypeId] = useState(1);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            // Using userId 1 as default for demonstration
            // In a real application, you would get this from authentication
            const userId = 1;
            await api.post(`/resources/${userId}`, {
                description,
                status,
                resource_type_id: resourceTypeId
            });
            navigate('/resources');
        } catch (err: any) {
            console.error('Error creating resource:', err);
            setError(err.response?.data?.detail || 'Erro ao cadastrar recurso. Tente novamente.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: 500, margin: '2rem auto' }}>
            <h2>Cadastrar Novo Recurso</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 16 }}>
                    <label>Descrição:</label>
                    <textarea
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        required
                        style={{ width: '100%', padding: 8 }}
                    />
                </div>
                <div style={{ marginBottom: 16 }}>
                    <label>Status:</label>
                    <select
                        value={status}
                        onChange={e => setStatus(e.target.value)}
                        style={{ width: '100%', padding: 8 }}
                    >
                        <option value="available">Disponível</option>
                        <option value="taken">Em uso</option>
                        <option value="maintenance">Em manutenção</option>
                    </select>
                </div>
                <div style={{ marginBottom: 16 }}>
                    <label>Tipo de Recurso:</label>
                    <select
                        value={resourceTypeId}
                        onChange={e => setResourceTypeId(Number(e.target.value))}
                        style={{ width: '100%', padding: 8 }}
                    >
                        <option value="1">Tipo 1</option>
                        <option value="2">Tipo 2</option>
                        <option value="3">Tipo 3</option>
                    </select>
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
