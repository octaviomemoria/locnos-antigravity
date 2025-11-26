'use client';

import { useParams, useRouter } from 'next/navigation';
import { usePersonById } from '@/lib/hooks/usePerson';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

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

export default function PersonDetailPage() {
    const params = useParams();
    const router = useRouter();
    const id = params.id as string;

    const { data: person, isLoading, error } = usePersonById(id);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (error || !person) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                    <h2 className="text-xl font-bold text-red-700 mb-2">Pessoa não encontrada</h2>
                    <p className="text-red-600">A pessoa solicitada não existe ou foi removida.</p>
                    <Button onClick={() => router.push('/dashboard/pessoas')} className="mt-4">
                        Voltar para listagem
                    </Button>
                </div>
            </div>
        );
    }

    const displayName = person.full_name || person.company_name || 'Sem nome';
    const isPF = !!person.cpf;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <Button
                        variant="outline"
                        onClick={() => router.push('/dashboard/pessoas')}
                        className="mb-4"
                    >
                        ← Voltar
                    </Button>
                    <h1 className="text-3xl font-bold text-gray-900">{displayName}</h1>
                    <div className="flex gap-2 mt-2">
                        {person.types.map((type) => getTypeBadge(type))}
                    </div>
                </div>
                <div className="flex gap-2">
                    {getStatusBadge(person.status)}
                </div>
            </div>

            {/* Documentos */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4">Documentos</h2>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="text-sm font-medium text-gray-500">
                            {isPF ? 'CPF' : 'CNPJ'}
                        </label>
                        <p className="text-gray-900 font-mono">
                            {person.cpf || person.cnpj || '-'}
                        </p>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-500">
                            {isPF ? 'RG' : 'IE'}
                        </label>
                        <p className="text-gray-900">{person.rg || person.ie || '-'}</p>
                    </div>
                </div>
            </div>

            {/* Contato */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-xl font-semibold mb-4">Informações de Contato</h2>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="text-sm font-medium text-gray-500">Telefone</label>
                        <p className="text-gray-900">{person.phone}</p>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-500">E-mail</label>
                        <p className="text-gray-900">{person.email || '-'}</p>
                    </div>
                    {person.address && (
                        <div className="col-span-2">
                            <label className="text-sm font-medium text-gray-500">Endereço</label>
                            <p className="text-gray-900">{person.address}</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Referências (se for Cliente ou Freteiro) */}
            {(person.types.includes('CLIENT') || person.types.includes('DRIVER')) &&
                person.references &&
                person.references.length > 0 && (
                    <div className="bg-white rounded-lg border border-gray-200 p-6">
                        <h2 className="text-xl font-semibold mb-4">Referências</h2>
                        <div className="space-y-4">
                            {person.references.map((ref: any, index: number) => (
                                <div key={index} className="border-l-4 border-blue-500 pl-4">
                                    <p className="font-medium text-gray-900">{ref.name}</p>
                                    <p className="text-sm text-gray-600">{ref.phone}</p>
                                    {ref.relationship && (
                                        <p className="text-sm text-gray-500">{ref.relationship}</p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

            {/* Informações Adicionais */}
            {person.notes && (
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                    <h2 className="text-xl font-semibold mb-4">Observações</h2>
                    <p className="text-gray-900">{person.notes}</p>
                </div>
            )}

            {/* Ações */}
            <div className="flex gap-3">
                <Button variant="default">Editar Pessoa</Button>
                <Button variant="destructive">Excluir Pessoa</Button>
            </div>
        </div>
    );
}
