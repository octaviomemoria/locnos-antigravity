'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useEquipment } from '@/lib/hooks/useEquipment';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import type { Equipment } from '@/types';
import { EquipmentModal } from '@/components/forms/EquipmentModal';

const getStatusBadge = (status: string) => {
    const variants: Record<string, { label: string; className: string }> = {
        AVAILABLE: { label: 'Disponível', className: 'bg-green-100 text-green-700' },
        RENTED: { label: 'Alugado', className: 'bg-orange-100 text-orange-700' },
        MAINTENANCE: { label: 'Manutenção', className: 'bg-red-100 text-red-700' },
        UNAVAILABLE: { label: 'Indisponível', className: 'bg-gray-100 text-gray-700' },
    };

    const variant = variants[status] || { label: status, className: '' };
    return (
        <Badge className={variant.className} variant="outline">
            {variant.label}
        </Badge>
    );
};

export default function EquipamentosPage() {
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [modalOpen, setModalOpen] = useState(false);
    const router = useRouter();

    const { data, isLoading, error } = useEquipment({
        page,
        per_page: 20,
        search: search || undefined,
    });

    if (error) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <p className="text-red-700">Erro ao carregar equipamentos: {String(error)}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Equipamentos</h1>
                    <p className="text-gray-600 mt-1">
                        Gerencie todos os equipamentos disponíveis para locação
                    </p>
                </div>
                <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    onClick={() => setModalOpen(true)}
                >
                    + Novo Equipamento
                </button>
            </div>

            {/* Filtros */}
            <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Buscar
                        </label>
                        <Input
                            placeholder="Nome, código ou marca..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Status
                        </label>
                        <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                            <option value="">Todos</option>
                            <option value="AVAILABLE">Disponível</option>
                            <option value="RENTED">Alugado</option>
                            <option value="MAINTENANCE">Manutenção</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Categoria
                        </label>
                        <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                            <option value="">Todas</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Tabela */}
            <div className="bg-white rounded-lg border border-gray-200">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <p className="text-gray-600 mt-4">Carregando equipamentos...</p>
                    </div>
                ) : data?.items && data.items.length > 0 ? (
                    <>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Nome</TableHead>
                                    <TableHead>Marca</TableHead>
                                    <TableHead>Código</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Quantidade</TableHead>
                                    <TableHead>Períodos</TableHead>
                                    <TableHead className="text-right">Ações</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {data.items.map((equipment: Equipment) => (
                                    <TableRow key={equipment.id}>
                                        <TableCell className="font-medium">{equipment.name}</TableCell>
                                        <TableCell>{equipment.brand || '-'}</TableCell>
                                        <TableCell className="font-mono text-sm">
                                            {equipment.internal_code}
                                        </TableCell>
                                        <TableCell>{getStatusBadge(equipment.status)}</TableCell>
                                        <TableCell>
                                            <span className="text-green-600 font-medium">
                                                {equipment.quantity_available}
                                            </span>
                                            <span className="text-gray-400"> / {equipment.quantity_total}</span>
                                        </TableCell>
                                        <TableCell>
                                            <span className="text-sm text-gray-600">
                                                {equipment.rental_periods?.length || 0} períodos
                                            </span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <button
                                                className="text-blue-600 hover:text-blue-700 text-sm font-medium cursor-pointer"
                                                onClick={() => router.push(`/dashboard/equipamentos/${equipment.id}`)}
                                            >
                                                Ver detalhes
                                            </button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>

                        {/* Paginação */}
                        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-200">
                            <p className="text-sm text-gray-600">
                                Mostrando {data.items.length} de {data.total} equipamentos
                            </p>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                                    disabled={page === 1}
                                    className="px-3 py-1 border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50"
                                >
                                    Anterior
                                </button>
                                <button
                                    onClick={() => setPage((p) => p + 1)}
                                    disabled={page >= (data.pages || 1)}
                                    className="px-3 py-1 border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50"
                                >
                                    Próxima
                                </button>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="p-12 text-center">
                        <p className="text-gray-600">Nenhum equipamento encontrado</p>
                        <p className="text-sm text-gray-400 mt-2">
                            Ajuste os filtros ou adicione novos equipamentos
                        </p>
                    </div>
                )}
            </div>

            <EquipmentModal open={modalOpen} onClose={() => setModalOpen(false)} />
        </div>
    );
}
