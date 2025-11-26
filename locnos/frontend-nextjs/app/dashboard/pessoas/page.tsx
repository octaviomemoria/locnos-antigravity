'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { personService } from '@/lib/api/person';
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
import type { Person } from '@/types';
import { PersonModal } from '@/components/forms/PersonModal';

const getTypeBadge = (type: string) => {
    const variants: Record<string, { label: string; className: string }> = {
        CLIENT: { label: 'Cliente', className: 'bg-blue-100 text-blue-700' },
        EMPLOYEE: { label: 'Funcionário', className: 'bg-purple-100 text-purple-700' },
        DRIVER: { label: 'Freteiro', className: 'bg-orange-100 text-orange-700' },
        SUPPLIER: { label: 'Fornecedor', className: 'bg-green-100 text-green-700' },
        PARTNER: { label: 'Parceiro', className: 'bg-pink-100 text-pink-700' },
    };

    const variant = variants[type] || { label: type, className: '' };
    return (
        <Badge className={variant.className} variant="outline" key={type}>
            {variant.label}
        </Badge>
    );
};

const getStatusBadge = (status: string) => {
    const variants: Record<string, { label: string; className: string }> = {
        PENDING: { label: 'Pendente', className: 'bg-yellow-100 text-yellow-700' },
        APPROVED: { label: 'Aprovado', className: 'bg-green-100 text-green-700' },
        REJECTED: { label: 'Rejeitado', className: 'bg-red-100 text-red-700' },
    };

    const variant = variants[status] || { label: status, className: '' };
    return (
        <Badge className={variant.className} variant="outline">
            {variant.label}
        </Badge>
    );
};

export default function PessoasPage() {
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [typeFilter, setTypeFilter] = useState('');
    const [modalOpen, setModalOpen] = useState(false);
    const router = useRouter();

    const { data, isLoading, error } = useQuery({
        queryKey: ['persons', page, search, typeFilter],
        queryFn: () =>
            personService.getAll({
                page,
                per_page: 20,
                search: search || undefined,
                person_type: typeFilter || undefined,
            }),
    });

    if (error) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <p className="text-red-700">Erro ao carregar pessoas: {String(error)}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Pessoas</h1>
                    <p className="text-gray-600 mt-1">
                        Clientes, fornecedores, freteiros e parceiros
                    </p>
                </div>
                <button
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    onClick={() => setModalOpen(true)}
                >
                    + Nova Pessoa
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
                            placeholder="Nome, email ou CPF/CNPJ..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Tipo
                        </label>
                        <select
                            className="w-full px-3 py-2 border border-gray-200 rounded-lg"
                            value={typeFilter}
                            onChange={(e) => setTypeFilter(e.target.value)}
                        >
                            <option value="">Todos</option>
                            <option value="CLIENT">Cliente</option>
                            <option value="DRIVER">Freteiro</option>
                            <option value="SUPPLIER">Fornecedor</option>
                            <option value="EMPLOYEE">Funcionário</option>
                            <option value="PARTNER">Parceiro</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Status
                        </label>
                        <select className="w-full px-3 py-2 border border-gray-200 rounded-lg">
                            <option value="">Todos</option>
                            <option value="APPROVED">Aprovado</option>
                            <option value="PENDING">Pendente</option>
                            <option value="REJECTED">Rejeitado</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Tabela */}
            <div className="bg-white rounded-lg border border-gray-200">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <p className="text-gray-600 mt-4">Carregando pessoas...</p>
                    </div>
                ) : data?.items && data.items.length > 0 ? (
                    <>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Nome</TableHead>
                                    <TableHead>Documento</TableHead>
                                    <TableHead>Telefone</TableHead>
                                    <TableHead>Tipos</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Ações</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {data.items.map((person: Person) => (
                                    <TableRow key={person.id}>
                                        <TableCell className="font-medium">
                                            {person.full_name || person.company_name}
                                        </TableCell>
                                        <TableCell className="font-mono text-sm">
                                            {person.cpf || person.cnpj || '-'}
                                        </TableCell>
                                        <TableCell>{person.phone}</TableCell>
                                        <TableCell>
                                            <div className="flex gap-1 flex-wrap">
                                                {person.types.map((type) => getTypeBadge(type))}
                                            </div>
                                        </TableCell>
                                        <TableCell>{getStatusBadge(person.status)}</TableCell>
                                        <TableCell className="text-right">
                                            <button
                                                className="text-blue-600 hover:text-blue-700 text-sm font-medium cursor-pointer"
                                                onClick={() => router.push(`/dashboard/pessoas/${person.id}`)}
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
                                Mostrando {data.items.length} de {data.total} pessoas
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
                        <p className="text-gray-600">Nenhuma pessoa encontrada</p>
                        <p className="text-sm text-gray-400 mt-2">
                            Ajuste os filtros ou adicione novas pessoas
                        </p>
                    </div>
                )}
            </div>

            <PersonModal open={modalOpen} onClose={() => setModalOpen(false)} />
        </div>
    );
}
