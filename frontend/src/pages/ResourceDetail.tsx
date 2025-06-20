import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

interface Resource {
    id: number;
    name: string;
    description: string;
}

const ResourceDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [resource, setResource] = useState<Resource | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchResource = async () => {
            try {
                const response = await api.get(`/resources/${id}`);
                setResource(response.data);
            } catch (err) {
                setError('Recurso não encontrado.');
            } finally {
                setLoading(false);
            }
        };
        fetchResource();
    }, [id]);

    if (loading) return <div>Carregando...</div>;
    if (error) return <div style={{ color: 'red' }}>{error}</div>;
    if (!resource) return null;

    return (
        <div style={{ maxWidth: 600, margin: '2rem auto' }}>
            <h2>Detalhes do Recurso</h2>
            <p><strong>ID:</strong> {resource.id}</p>
            <p><strong>Nome:</strong> {resource.name}</p>
            <p><strong>Descrição:</strong> {resource.description}</p>
            <Link to="/resources">Voltar para lista</Link>
        </div>
    );
};

export default ResourceDetail;
