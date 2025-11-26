'use client';

import { useAuthStore } from '@/lib/store/auth';

export default function DashboardPage() {
    const user = useAuthStore((state) => state.user);

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
                            <p className="text-3xl font-bold text-gray-900 mt-2">4</p>
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
                            <p className="text-3xl font-bold text-green-600 mt-2">2</p>
                        </div>
                        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">
                            ✅
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Alugados</p>
                            <p className="text-3xl font-bold text-orange-600 mt-2">2</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center text-2xl">
                            📦
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Pessoas</p>
                            <p className="text-3xl font-bold text-purple-600 mt-2">4</p>
                        </div>
                        <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
                            👥
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
                        href="/dashboard/categorias"
                        className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
                    >
                        <span className="text-2xl mr-3">📁</span>
                        <span className="font-medium">Nova Categoria</span>
                    </a>
                </div>
            </div>

            {/* System Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                    🎉 Sistema Funcionando!
                </h3>
                <p className="text-blue-700">
                    Backend FastAPI integrado com sucesso. 21 endpoints disponíveis.
                    <br />
                    Dados: 4 equipamentos, 4 pessoas, 4 categorias, 10 subcategorias.
                </p>
            </div>
        </div>
    );
}
