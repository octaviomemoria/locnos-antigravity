import axios from 'axios';
import { deleteCookie, getCookie, setCookie } from 'cookies-next';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = getCookie('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
export const auth = {
    setToken: (token: string) => {
        setCookie('token', token, { maxAge: 60 * 60 * 24 * 7 }); // 7 days
    },
    getToken: () => {
        const token = getCookie('token');
        return typeof token === 'string' ? token : undefined;
    },
    removeToken: () => {
        deleteCookie('token');
    },
    isAuthenticated: () => {
        return !!getCookie('token');
    },
};
