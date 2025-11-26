import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { equipmentService } from '@/lib/api/equipment';
import type { Equipment } from '@/types';

export function useEquipment(params?: {
    page?: number;
    per_page?: number;
    search?: string;
    category_id?: string;
    status?: string;
}) {
    return useQuery({
        queryKey: ['equipment', params],
        queryFn: () => equipmentService.getAll(params),
    });
}

export function useEquipmentById(id: string) {
    return useQuery({
        queryKey: ['equipment', id],
        queryFn: () => equipmentService.getById(id),
        enabled: !!id,
    });
}

export function useCreateEquipment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Equipment>) => equipmentService.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['equipment'] });
        },
    });
}

export function useUpdateEquipment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Equipment> }) =>
            equipmentService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['equipment'] });
        },
    });
}

export function useDeleteEquipment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => equipmentService.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['equipment'] });
        },
    });
}
