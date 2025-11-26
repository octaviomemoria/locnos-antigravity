'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEquipmentById } from '@/lib/hooks/useEquipment';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

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

export default function EquipmentDetailPage() {
    const params = useParams();
    const router = useRouter();
    const id = params.id as string;

    const { data: equipment, isLoading, error } = useEquipmentById(id);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (error || !equipment) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <h2 className="text-xl font-bold text-red-700 mb-2">Equipamento não encontrado</h2>
                    <p className="text-red-600">O equipamento solicitado não existe ou foi removido.</p>
                    <Button onClick={() => router.push('/dashboard/equipamentos')} className="mt-4">
                        Voltar para listagem
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <Button
                        variant="outline"
                        onClick={() => router.push('/dashboard/equipamentos')}
                        className="mb-4"
                    >
                        ← Voltar
                    </Button>
                    <h1 className="text-3xl font-bold text-gray-900">{equipment.name}</h1>
                    <p className="text-gray-600 mt-1">Código: {equipment.internal_code}</p>
                </div>
                <div className="flex gap-2">
                    {getStatusBadge(equipment.status)}
                </div>
            </div>

            {/* Informações Básicas */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4">Informações Básicas</h2>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="text-sm font-medium text-gray-500">Marca</label>
                        <p className="text-gray-900">{equipment.brand || '-'}</p>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-500">Categoria</label>
                        <p className="text-gray-900">{equipment.category?.name || '-'}</p>
                    </div>
                    <div className="col-span-2">
                        <label className="text-sm font-medium text-gray-500">Descrição</label>
                        <p className="text-gray-900">{equipment.description || '-'}</p>
                    </div>
                </div>
            </div>

            {/* Quantidade e Disponibilidade */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-500 mb-2">Quantidade Total</h3>
                    <p className="text-3xl font-bold text-gray-900">{equipment.quantity_total}</p>
                </div>
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-500 mb-2">Disponível</h3>
                    <p className="text-3xl font-bold text-green-600">{equipment.quantity_available}</p>
                </div>
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-500 mb-2">Em Uso</h3>
                    <p className="text-3xl font-bold text-orange-600">
                        {equipment.quantity_total - equipment.quantity_available}
                    </p>
                </div>
            </div>

            {/* Períodos de Locação */}
            {equipment.rental_periods && equipment.rental_periods.length > 0 && (
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h2 className="text-xl font-semibold mb-4">Períodos de Locação</h2>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Descrição</TableHead>
                                <TableHead>Valor</TableHead>
                                <TableHead>Tipo</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {equipment.rental_periods.map((period: any) => (
                                <TableRow key={period.id}>
                                    <TableCell>{period.description}</TableCell>
                                    <TableCell>R$ {period.value?.toFixed(2) || '0.00'}</TableCell>
                                    <TableCell>{period.period_type}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            )}

            {/* Ações */}
            <div className="flex gap-3">
                <Button variant="default">Editar Equipamento</Button>
                <Button variant="destructive">Excluir Equipamento</Button>
            </div>
        </div>
    );
}
