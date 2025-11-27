import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { api, auth } from '@/lib/auth';
import type { User, LoginCredentials, AuthResponse } from '@/types';

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;

    login: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
    setAuth: (user: User, token: string) => void;
    checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set, get) => ({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,

            login: async (credentials: LoginCredentials) => {
                set({ isLoading: true });
                try {
                    // 1. Login
                    const response = await api.post<AuthResponse>('/auth/login', credentials);
                    const { access_token } = response.data;

                    // 2. Salvar token
                    auth.setToken(access_token);

                    // 3. Buscar dados do usuário
                    const userResponse = await api.get<User>('/auth/me');
                    const user = userResponse.data;

                    // 4. Atualizar store
                    set({
                        user,
                        token: access_token,
                        isAuthenticated: true,
                        isLoading: false,
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            logout: () => {
                auth.removeToken();
                set({
                    user: null,
                    token: null,
                    isAuthenticated: false,
                });
            },

            setAuth: (user: User, token: string) => {
                auth.setToken(token);
                set({
                    user,
                    token,
                    isAuthenticated: true,
                });
            },

            checkAuth: () => {
                const token = auth.getToken();
                if (token) {
                    set({ isAuthenticated: true, token });
                } else {
                    set({ isAuthenticated: false, token: null, user: null });
                }
            }
        }),
        {
            name: 'auth-storage',
            storage: createJSONStorage(() => localStorage),
            partialize: (state) => ({
                user: state.user,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);

