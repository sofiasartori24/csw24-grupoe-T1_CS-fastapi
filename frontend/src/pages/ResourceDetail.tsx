import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Resource {
    id: number;
    description: string;
    status: string;
    resource_type_id: number;
}

const ResourceDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [resource, setResource] = useState<Resource | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    
    const handleReserveClick = () => {
        navigate(`/resources/${id}/reserve`);
    };

    useEffect(() => {
        const fetchResource = async () => {
            try {
                const response = await api.get(`/resources/${id}`);
                setResource(response.data);
            } catch (err: any) {
                console.error('Error fetching resource details:', err);
                setError(err.response?.data?.detail || 'Recurso não encontrado ou erro de conexão.');
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
            <p><strong>Descrição:</strong> {resource.description}</p>
            <p><strong>Status:</strong> <span style={{ color: getStatusColor(resource.status) }}>{resource.status}</span></p>
            <p><strong>Tipo de Recurso ID:</strong> {resource.resource_type_id}</p>
            
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <Link to="/resources" style={{ padding: '8px 16px', textDecoration: 'none', color: '#1976d2' }}>
                    Voltar para lista
                </Link>
                
                {resource.status === 'available' && (
                    <button
                        onClick={handleReserveClick}
                        style={{
                            padding: '8px 16px',
                            backgroundColor: '#1976d2',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Fazer Reserva
                    </button>
                )}
            </div>
        </div>
    );

    // Helper function to get color based on status
    function getStatusColor(status: string): string {
        switch (status.toLowerCase()) {
            case 'available':
                return 'green';
            case 'taken':
                return 'orange';
            case 'maintenance':
                return 'red';
            default:
                return 'gray';
        }
    }
};

export default ResourceDetail;
