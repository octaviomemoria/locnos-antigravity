'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { personService } from '@/lib/api/person';

const personSchema = z.object({
    types: z.array(z.string()).min(1, 'Selecione pelo menos um tipo'),
    document_type: z.enum(['CPF', 'CNPJ']),
    full_name: z.string().optional(),
    company_name: z.string().optional(),
    cpf: z.string().optional(),
    cnpj: z.string().optional(),
    phone: z.string().min(10, 'Telefone deve ter no mínimo 10 dígitos'),
    email: z.string().email('E-mail inválido').optional(),
});

type PersonFormData = z.infer<typeof personSchema>;

interface PersonModalProps {
    open: boolean;
    onClose: () => void;
}

const PERSON_TYPES = [
    { value: 'CLIENT', label: 'Cliente' },
    { value: 'DRIVER', label: 'Freteiro' },
    { value: 'SUPPLIER', label: 'Fornecedor' },
    { value: 'EMPLOYEE', label: 'Funcionário' },
    { value: 'PARTNER', label: 'Parceiro' },
];

export function PersonModal({ open, onClose, person: initialPerson }: PersonModalProps) {
    const person = initialPerson as any;
    const queryClient = useQueryClient();
    const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
    const [documentType, setDocumentType] = useState<'CPF' | 'CNPJ'>('CPF');

    const {
        register,
        handleSubmit,
        formState: { errors },
        reset,
        setValue,
    } = useForm<PersonFormData>({
        resolver: zodResolver(personSchema),
        defaultValues: {
            types: [],
            document_type: 'CPF',
        },
    });

    const createPerson = useMutation({
        mutationFn: (data: any) => personService.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['persons'] });
            reset();
            setSelectedTypes([]);
            onClose();
            alert('✅ Pessoa criada com sucesso!');
        },
        onError: (error: any) => {
            alert(`Erro ao criar pessoa: ${error.response?.data?.detail || error.message}`);
        },
    });

    const toggleType = (type: string) => {
        const newTypes = selectedTypes.includes(type)
            ? selectedTypes.filter((t) => t !== type)
            : [...selectedTypes, type];
        setSelectedTypes(newTypes);
        setValue('types', newTypes);
    };

    const onSubmit = async (data: PersonFormData) => {
        const payload: any = {
            types: selectedTypes,
            phone: data.phone,
            email: data.email || null,
            status: 'PENDING',
        };

        if (documentType === 'CPF') {
            payload.cpf = data.cpf;
            payload.full_name = data.full_name;
        } else {
            payload.cnpj = data.cnpj;
            payload.company_name = data.company_name;
        }

        createPerson.mutate(payload);
    };

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Nova Pessoa</DialogTitle>
                    <DialogDescription>
                        Adicione um cliente, fornecedor, freteiro ou parceiro
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    {/* Tipos */}
                    <div>
                        <Label>Tipos * (pode selecionar múltiplos)</Label>
                        <div className="grid grid-cols-2 gap-2 mt-2">
                            {PERSON_TYPES.map((type) => (
                                <div key={type.value} className="flex items-center space-x-2">
                                    <Checkbox
                                        id={type.value}
                                        checked={selectedTypes.includes(type.value)}
                                        onCheckedChange={() => toggleType(type.value)}
                                    />
                                    <label
                                        htmlFor={type.value}
                                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                                    >
                                        {type.label}
                                    </label>
                                </div>
                            ))}
                        </div>
                        {errors.types && (
                            <p className="text-sm text-red-600 mt-1">{errors.types.message}</p>
                        )}
                    </div>

                    {/* Tipo de Documento */}
                    <div>
                        <Label>Tipo de Documento *</Label>
                        <div className="flex gap-4 mt-2">
                            <label className="flex items-center space-x-2 cursor-pointer">
                                <input
                                    type="radio"
                                    value="CPF"
                                    checked={documentType === 'CPF'}
                                    onChange={() => {
                                        setDocumentType('CPF');
                                        setValue('document_type', 'CPF');
                                    }}
                                />
                                <span className="text-sm">CPF (Pessoa Física)</span>
                            </label>
                            <label className="flex items-center space-x-2 cursor-pointer">
                                <input
                                    type="radio"
                                    value="CNPJ"
                                    checked={documentType === 'CNPJ'}
                                    onChange={() => {
                                        setDocumentType('CNPJ');
                                        setValue('document_type', 'CNPJ');
                                    }}
                                />
                                <span className="text-sm">CNPJ (Pessoa Jurídica)</span>
                            </label>
                        </div>
                    </div>

                    {/* Campos Condicionais */}
                    <div className="grid grid-cols-2 gap-4">
                        {documentType === 'CPF' ? (
                            <>
                                <div className="col-span-2">
                                    <Label htmlFor="full_name">Nome Completo *</Label>
                                    <Input id="full_name" {...register('full_name')} />
                                </div>
                                <div>
                                    <Label htmlFor="cpf">CPF *</Label>
                                    <Input id="cpf" {...register('cpf')} placeholder="000.000.000-00" />
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="col-span-2">
                                    <Label htmlFor="company_name">Razão Social *</Label>
                                    <Input id="company_name" {...register('company_name')} />
                                </div>
                                <div>
                                    <Label htmlFor="cnpj">CNPJ *</Label>
                                    <Input id="cnpj" {...register('cnpj')} placeholder="00.000.000/0000-00" />
                                </div>
                            </>
                        )}

                        <div>
                            <Label htmlFor="phone">Telefone *</Label>
                            <Input id="phone" {...register('phone')} placeholder="(00) 00000-0000" />
                            {errors.phone && (
                                <p className="text-sm text-red-600 mt-1">{errors.phone.message}</p>
                            )}
                        </div>

                        <div className="col-span-2">
                            <Label htmlFor="email">E-mail</Label>
                            <Input id="email" type="email" {...register('email')} />
                            {errors.email && (
                                <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
                            )}
                        </div>
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={onClose}>
                            Cancelar
                        </Button>
                        <Button type="submit" disabled={createPerson.isPending}>
                            {createPerson.isPending ? 'Criando...' : 'Criar Pessoa'}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
