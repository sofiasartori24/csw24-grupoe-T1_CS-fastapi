import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

interface Resource {
    id: number;
    name: string;
    // Adicione outros campos conforme sua API
}

const Resources: React.FC = () => {
    const [resources, setResources] = useState<Resource[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadResources = async () => {
            try {
                const response = await api.get("/resources");
                setResources(response.data);
            } catch (err: any) {
                setError("Erro ao carregar recursos");
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
                            <Link to={`/resources/${resource.id}`}>{resource.name}</Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Resources;
