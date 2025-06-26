import axios from "axios";

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "https://1jjdwnh7k5.execute-api.us-east-1.amazonaws.com/Prod",
    headers: {
        "Content-Type": "application/json",
        // Add headers that might be used by Swagger UI
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        // Disable preflight caching to ensure fresh requests
        "Cache-Control": "no-cache"
    },
    // Ensure credentials aren't sent with cross-origin requests
    withCredentials: false
});

// Add a request interceptor to modify requests before they're sent
api.interceptors.request.use(
    (config) => {
        // For DELETE requests, try to make them more compatible with the API
        if (config.method === 'delete') {
            // Some APIs expect the DELETE method to be uppercase
            config.method = 'DELETE';
            
            // Add query parameter as an alternative way to specify the method
            if (config.url && !config.url.includes('_method=')) {
                config.url += (config.url.includes('?') ? '&' : '?') + '_method=DELETE';
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Request interceptor for logging and debugging
api.interceptors.request.use(
    (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, {
            headers: config.headers,
            data: config.data,
            params: config.params
        });
        return config;
    },
    (error) => {
        console.error("API Request Error:", error);
        return Promise.reject(error);
    }
);

// Response interceptor for logging and debugging
api.interceptors.response.use(
    (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`, {
            data: response.data,
            headers: response.headers
        });
        return response;
    },
    (error) => {
        console.error("API Response Error:", error);
        if (error.response) {
            console.error("Error Details:", {
                status: error.response.status,
                statusText: error.response.statusText,
                data: error.response.data,
                headers: error.response.headers
            });
        } else if (error.request) {
            console.error("No response received:", error.request);
        } else {
            console.error("Error setting up request:", error.message);
        }
        return Promise.reject(error);
    }
);

export default api;