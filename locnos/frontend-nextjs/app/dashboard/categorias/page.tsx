'use client';

import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api/client';
import { Badge } from '@/components/ui/badge';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

export default function CategoriasPage() {
    const { data: categories, isLoading } = useQuery({
        queryKey: ['categories'],
        queryFn: async () => {
            const response = await api.get('/categories/');
            return response.data;
        },
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Categorias</h1>
                    <p className="text-gray-600 mt-1">
                        Gerencie categorias e subcategorias de equipamentos
                    </p>
                </div>
                <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    onClick={() => alert('Modal de criar categoria em desenvolvimento')}
                >
                    + Nova Categoria
                </button>
            </div>

            {/* Tabela */}
            <div className="bg-white rounded-lg border border-gray-200">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <p className="text-gray-600 mt-4">Carregando categorias...</p>
                    </div>
                ) : categories?.length > 0 ? (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Nome</TableHead>
                                <TableHead>Slug</TableHead>
                                <TableHead>Descrição</TableHead>
                                <TableHead>Total Equipamentos</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Ações</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {categories.map((category: any) => (
                                <TableRow key={category.id}>
                                    <TableCell className="font-medium">
                                        <div className="flex items-center gap-2">
                                            {category.icon && <span>{category.icon}</span>}
                                            {category.name}
                                        </div>
                                    </TableCell>
                                    <TableCell className="font-mono text-sm">{category.slug}</TableCell>
                                    <TableCell className="text-gray-600">
                                        {category.description || '-'}
                                    </TableCell>
                                    <TableCell>
                                        <span className="text-blue-600 font-medium">
                                            {category.total_equipment || 0}
                                        </span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant={category.active ? 'default' : 'secondary'}>
                                            {category.active ? 'Ativa' : 'Inativa'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                                            Ver subcategorias
                                        </button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                ) : (
                    <div className="p-12 text-center">
                        <p className="text-gray-600">Nenhuma categoria encontrada</p>
                    </div>
                )}
            </div>
        </div>
    );
}
