import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Helper function to get auth token from localStorage or Zustand persisted state
const getAuthToken = (): string | null => {
    if (typeof window === 'undefined') return null;

    // First try the direct localStorage key
    let token = localStorage.getItem('access_token');

    // If not found, try to get from Zustand's persisted state
    if (!token) {
        try {
            const authStorage = localStorage.getItem('auth-storage');
            if (authStorage) {
                const parsed = JSON.parse(authStorage);
                token = parsed?.state?.accessToken || null;
                // Sync it to the direct key for future requests
                if (token) {
                    localStorage.setItem('access_token', token);
                }
            }
        } catch (e) {
            console.error('Error parsing auth-storage:', e);
        }
    }

    return token;
};

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = getAuthToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                // TODO: Implement refresh token endpoint
                // const response = await axios.post(`${API_URL}/api/auth/refresh`, { refresh_token: refreshToken });
                // localStorage.setItem('access_token', response.data.access_token);
                // return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/auth/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api;

// Auth API
export const authAPI = {
    register: (data: { email: string; password: string; role?: string }) =>
        api.post('/api/auth/register', data),

    login: (data: { email: string; password: string }) =>
        api.post('/api/auth/login', data),

    googleAuth: (credential: string) =>
        api.post('/api/auth/google', { credential }),

    onboard: (data: { college_name?: string; semester?: number; subjects?: string[]; language?: string }) =>
        api.post('/api/auth/onboard', data),
};

// Projects API
export const projectsAPI = {
    generate: (data: { subject: string; semester: number; difficulty: string; additional_requirements?: string }) =>
        api.post('/api/projects/generate', data),

    getStatus: (jobId: string) =>
        api.get(`/api/projects/${jobId}/status`),

    getPreview: (jobId: string) =>
        api.get(`/api/projects/${jobId}/preview`),

    getDownload: (jobId: string) =>
        api.get(`/api/projects/${jobId}/download`),

    getHistory: () =>
        api.get('/api/projects/history'),
};

// Admin API
export const adminAPI = {
    getUsageStats: () =>
        api.get('/api/admin/usage'),

    getAuditLogs: (limit?: number) =>
        api.get('/api/admin/audit-logs', { params: { limit } }),
};

// Payments API
export const paymentsAPI = {
    getPlans: () =>
        api.get('/api/payments/plans'),

    getSubscription: () =>
        api.get('/api/payments/subscription'),

    createOrder: (plan: string = 'pro') =>
        api.post('/api/payments/create-order', { plan }),

    verifyPayment: (data: { razorpay_payment_id: string; razorpay_order_id?: string; plan: string }) =>
        api.post('/api/payments/verify', data),

    getHistory: () =>
        api.get('/api/payments/history'),
};

