import axios from "axios";

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "https://1jjdwnh7k5.execute-api.us-east-1.amazonaws.com/Prod",
    headers: {
        "Content-Type": "application/json",
    },
});

export default api;