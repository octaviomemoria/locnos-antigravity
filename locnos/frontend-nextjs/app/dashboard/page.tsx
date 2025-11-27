'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store/auth';
import { api } from '@/lib/auth';

interface DashboardStats {
    orders: {
        total: number;
        pending: number;
        in_transit: number;
    };
    equipment: {
        total: number;
        available: number;
    };
    fleet: {
        active_vehicles: number;
    };
}

export default function DashboardPage() {
    const user = useAuthStore((state) => state.user);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.get<DashboardStats>('/dashboard/stats');
                setStats(response.data);
            } catch (error) {
                console.error('Erro ao buscar estatísticas:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) {
        return <div className="p-6">Carregando dashboard...</div>;
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600 mt-1">
                    Bem-vindo, {user?.name || 'Usuário'}!
                </p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Total Equipamentos</p>
                            <p className="text-3xl font-bold text-gray-900 mt-2">
                                {stats?.equipment.total || 0}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">
                            🔧
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Disponíveis</p>
                            <p className="text-3xl font-bold text-green-600 mt-2">
                                {stats?.equipment.available || 0}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">
                            ✅
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Pedidos Pendentes</p>
                            <p className="text-3xl font-bold text-orange-600 mt-2">
                                {stats?.orders.pending || 0}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center text-2xl">
                            📦
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Em Rota</p>
                            <p className="text-3xl font-bold text-purple-600 mt-2">
                                {stats?.orders.in_transit || 0}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
                            🚚
                        </div>
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Ações Rápidas</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <a
                        href="/dashboard/equipamentos"
                        className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    >
                        <span className="text-2xl mr-3">➕</span>
                        <span className="font-medium">Novo Equipamento</span>
                    </a>
                    <a
                        href="/dashboard/pessoas"
                        className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    >
                        <span className="text-2xl mr-3">👤</span>
                        <span className="font-medium">Nova Pessoa</span>
                    </a>
                    <a
                        href="/dashboard/pedidos"
                        className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    >
                        <span className="text-2xl mr-3">📝</span>
                        <span className="font-medium">Novo Pedido</span>
                    </a>
                </div>
            </div>

            {/* System Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                    🎉 Sistema Conectado!
                </h3>
                <p className="text-blue-700">
                    Dados atualizados em tempo real do backend.
                </p>
            </div>
        </div>
    );
}
