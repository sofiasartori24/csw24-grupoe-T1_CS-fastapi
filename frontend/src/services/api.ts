import axios from "axios";

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000", // ajuste se necessário
    headers: {
        "Content-Type": "application/json",
    },
});

export default api;