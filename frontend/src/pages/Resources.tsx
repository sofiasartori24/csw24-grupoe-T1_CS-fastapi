import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

interface Resource {
    id: number;
    description: string;
    status: string;
    resource_type_id: number;
}

const Resources: React.FC = () => {
    const [resources, setResources] = useState<Resource[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadResources = async () => {
            try {
                const response = await api.get("/resources/");
                setResources(response.data);
            } catch (err: any) {
                console.error("Error loading resources:", err);
                setError(err.response?.data?.detail || "Erro ao carregar recursos. Verifique sua conexão e tente novamente.");
            } finally {
                setLoading(false);
            }
        };
        loadResources();
    }, []);

    if (loading) return <div>Carregando recursos...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h2>Lista de Recursos</h2>
            <Link to="/resources/new" style={{ marginBottom: 16, display: 'inline-block' }}>
                + Novo Recurso
            </Link>
            {resources.length === 0 ? (
                <p>Nenhum recurso encontrado.</p>
            ) : (
                <ul>
                    {resources.map((resource) => (
                        <li key={resource.id}>
                            <Link to={`/resources/${resource.id}`}>{resource.description}</Link>
                            <span style={{ marginLeft: '10px', color: getStatusColor(resource.status) }}>
                                ({resource.status})
                            </span>
                        </li>
                    ))}
                </ul>
            )}
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

export default Resources;
