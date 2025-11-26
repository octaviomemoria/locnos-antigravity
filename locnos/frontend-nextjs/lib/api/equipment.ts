import api from './client';
import type { Equipment, EquipmentListResponse } from '@/types';

export const equipmentService = {
    // Listar equipamentos com filtros
    async getAll(params?: {
        page?: number;
        per_page?: number;
        search?: string;
        category_id?: string;
        status?: string;
    }): Promise<EquipmentListResponse> {
        const response = await api.get<EquipmentListResponse>('/equipment/', { params });
        return response.data;
    },

    // Obter um equipamento por ID
    async getById(id: string): Promise<Equipment> {
        const response = await api.get<Equipment>(`/equipment/${id}`);
        return response.data;
    },

    // Criar equipamento
    async create(data: Partial<Equipment>): Promise<Equipment> {
        const response = await api.post<Equipment>('/equipment/', data);
        return response.data;
    },

    // Atualizar equipamento
    async update(id: string, data: Partial<Equipment>): Promise<Equipment> {
        const response = await api.put<Equipment>(`/equipment/${id}`, data);
        return response.data;
    },

    // Deletar equipamento
    async delete(id: string): Promise<void> {
        await api.delete(`/equipment/${id}`);
    },
};
