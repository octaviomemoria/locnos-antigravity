'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();
    const { isAuthenticated, user, token } = useAuthStore();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Verificar apenas uma vez no mount
        const token = localStorage.getItem('access_token');
        if (!token) {
            router.push('/login');
        } else {
            setIsLoading(false);
        }
    }, []); // Array vazio = executa apenas no mount

    // Redirecionar se não autenticado
    useEffect(() => {
        if (!isLoading && !isAuthenticated && !token) {
            router.push('/login');
        }
    }, [isAuthenticated, token, isLoading, router]);

    if (isLoading || (!isAuthenticated && !token)) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Sidebar */}
            <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200">
                <div className="flex flex-col h-full">
                    {/* Logo */}
                    <div className="flex items-center h-16 px-6 border-b border-gray-200">
                        <h1 className="text-xl font-bold text-blue-600">Locnos</h1>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 px-4 py-6 space-y-1">
                        <a
                            href="/dashboard"
                            className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                        >
                            <span>📊 Dashboard</span>
                        </a>
                        <a
                            href="/dashboard/equipamentos"
                            className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                        >
                            <span>🔧 Equipamentos</span>
                        </a>
                        <a
                            href="/dashboard/pessoas"
                            className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                        >
                            <span>👥 Pessoas</span>
                        </a>
                        <a
                            href="/dashboard/categorias"
                            className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600 transition-colors"
                        >
                            <span>📁 Categorias</span>
                        </a>
                    </nav>

                    {/* User info */}
                    <div className="p-4 border-t border-gray-200">
                        <button
                            onClick={() => {
                                useAuthStore.getState().logout();
                                router.push('/login');
                            }}
                            className="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        >
                            Sair
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main content */}
            <main className="ml-64 p-8">{children}</main>
        </div>
    );
}
