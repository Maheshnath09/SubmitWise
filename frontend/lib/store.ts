import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
    id: string;
    email: string;
    role: string;
    credits: number;
    semester?: number;
    subjects?: string[];
    language?: string;
}

interface AuthState {
    user: User | null;
    accessToken: string | null;
    refreshToken: string | null;
    isAuthenticated: boolean;
    hasHydrated: boolean;

    setAuth: (user: User, accessToken: string, refreshToken: string) => void;
    logout: () => void;
    updateUser: (user: Partial<User>) => void;
    setHasHydrated: (state: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
            hasHydrated: false,

            setAuth: (user, accessToken, refreshToken) => {
                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);
                set({ user, accessToken, refreshToken, isAuthenticated: true });
            },

            logout: () => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false });
            },

            updateUser: (userData) => set((state) => ({
                user: state.user ? { ...state.user, ...userData } : null,
            })),

            setHasHydrated: (state) => set({ hasHydrated: state }),
        }),
        {
            name: 'auth-storage',
            onRehydrateStorage: () => (state) => {
                state?.setHasHydrated(true);
            },
        }
    )
);
