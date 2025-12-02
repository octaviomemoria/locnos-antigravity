'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
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
import { Textarea } from '@/components/ui/textarea';
import { useCreateEquipment, useUpdateEquipment } from '@/lib/hooks/useEquipment';
import type { Equipment } from '@/types';
import { equipmentSchema, type EquipmentFormData } from '@/lib/validations/schemas';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api/client';

interface EquipmentModalProps {
    open: boolean;
    onClose: () => void;
    equipment?: Equipment;
    mode?: 'create' | 'edit';
}

export function EquipmentModal({ open, onClose, equipment: initialEquipment, mode = 'create' }: EquipmentModalProps) {
    const equipment = initialEquipment as any;
    const createEquipment = useCreateEquipment();
    const updateEquipment = useUpdateEquipment();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const isEditMode = mode === 'edit';

    const {
        register,
        handleSubmit,
        formState: { errors },
        reset,
    } = useForm<EquipmentFormData>({
        resolver: zodResolver(equipmentSchema),
        defaultValues: equipment ? {
            name: equipment.name,
            brand: equipment.brand || '',
            internal_code: equipment.internal_code,
            description: equipment.description || '',
            category_id: equipment.category_id,
            quantity_total: equipment.quantity_total,
            rental_value: equipment.rental_value || undefined,
            status: equipment.status || 'AVAILABLE',
        } : {
            status: 'AVAILABLE',
            quantity_total: 1,
        },
    });

    const { data: categories } = useQuery({
        queryKey: ['categories'],
        queryFn: async () => {
            const response = await api.get('/categories/');
            return response.data;
        },
    });

    const onSubmit = async (data: EquipmentFormData) => {
        setIsSubmitting(true);
        try {
            if (isEditMode && equipment) {
                await updateEquipment.mutateAsync({ id: equipment.id, data: data as any });
                alert('✅ Equipamento atualizado com sucesso!');
            } else {
                await createEquipment.mutateAsync(data as any);
                alert('✅ Equipamento criado com sucesso!');
            }
            reset();
            onClose();
        } catch (error: any) {
            alert(`Erro ao ${isEditMode ? 'atualizar' : 'criar'} equipamento: ${error.response?.data?.detail || error.message}`);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>{isEditMode ? 'Editar Equipamento' : 'Novo Equipamento'}</DialogTitle>
                    <DialogDescription>
                        {isEditMode ? 'Atualize as informações do equipamento' : 'Adicione um novo equipamento ao catálogo'}
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="col-span-2">
                            <Label htmlFor="name">Nome *</Label>
                            <Input id="name" {...register('name')} placeholder="Ex: Betoneira 400L" />
                            {errors.name && (
                                <p className="text-sm text-red-600 mt-1">{errors.name.message}</p>
                            )}
                        </div>

                        <div>
                            <Label htmlFor="brand">Marca</Label>
                            <Input id="brand" {...register('brand')} placeholder="Ex: Vonder" />
                        </div>

                        <div>
                            <Label htmlFor="internal_code">Código Interno *</Label>
                            <Input id="internal_code" {...register('internal_code')} placeholder="Ex: BET-001" />
                            {errors.internal_code && (
                                <p className="text-sm text-red-600 mt-1">{errors.internal_code.message}</p>
                            )}
                        </div>

                        <div className="col-span-2">
                            <Label htmlFor="description">Descrição</Label>
                            <Textarea
                                id="description"
                                {...register('description')}
                                placeholder="Descreva o equipamento..."
                                rows={3}
                            />
                        </div>

                        <div>
                            <Label htmlFor="category_id">Categoria *</Label>
                            <select
                                id="category_id"
                                {...register('category_id')}
                                className="w-full px-3 py-2 border border-gray-200 rounded-lg"
                            >
                                <option value="">Selecione...</option>
                                {categories?.map((cat: any) => (
                                    <option key={cat.id} value={cat.id}>
                                        {cat.name}
                                    </option>
                                ))}
                            </select>
                            {errors.category_id && (
                                <p className="text-sm text-red-600 mt-1">{errors.category_id.message}</p>
                            )}
                        </div>

                        <div>
                            <Label htmlFor="quantity_total">Quantidade *</Label>
                            <Input
                                id="quantity_total"
                                type="number"
                                {...register('quantity_total', { valueAsNumber: true })}
                                min={1}
                            />
                            {errors.quantity_total && (
                                <p className="text-sm text-red-600 mt-1">{errors.quantity_total.message}</p>
                            )}
                        </div>

                        <div>
                            <Label htmlFor="rental_value">Valor Locação (R$)</Label>
                            <Input
                                id="rental_value"
                                type="number"
                                step="0.01"
                                {...register('rental_value', { valueAsNumber: true })}
                                placeholder="0.00"
                            />
                        </div>

                        <div>
                            <Label htmlFor="status">Status</Label>
                            <select
                                id="status"
                                {...register('status')}
                                className="w-full px-3 py-2 border border-gray-200 rounded-lg"
                            >
                                <option value="AVAILABLE">Disponível</option>
                                <option value="MAINTENANCE">Manutenção</option>
                                <option value="UNAVAILABLE">Indisponível</option>
                            </select>
                        </div>
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={onClose}>
                            Cancelar
                        </Button>
                        <Button type="submit" disabled={isSubmitting}>
                            {isSubmitting ? (isEditMode ? 'Salvando...' : 'Criando...') : (isEditMode ? 'Salvar Alterações' : 'Criar Equipamento')}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
