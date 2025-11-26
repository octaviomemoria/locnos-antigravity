import api from './client';
import type { Person, PersonListResponse } from '@/types';

export const personService = {
    // Listar pessoas com filtros
    async getAll(params?: {
        page?: number;
        per_page?: number;
        search?: string;
        person_type?: string;
        status?: string;
    }): Promise<PersonListResponse> {
        const response = await api.get<PersonListResponse>('/persons/', { params });
        return response.data;
    },

    // Obter uma pessoa por ID
    async getById(id: string): Promise<Person> {
        const response = await api.get<Person>(`/persons/${id}`);
        return response.data;
    },

    // Criar pessoa
    async create(data: Partial<Person>): Promise<Person> {
        const response = await api.post<Person>('/persons/', data);
        return response.data;
    },

    // Atualizar pessoa
    async update(id: string, data: Partial<Person>): Promise<Person> {
        const response = await api.put<Person>(`/persons/${id}`, data);
        return response.data;
    },

    // Deletar pessoa
    async delete(id: string): Promise<void> {
        await api.delete(`/persons/${id}`);
    },

    // Freteiros disponíveis
    async getAvailableDrivers(): Promise<Person[]> {
        const response = await api.get<Person[]>('/persons/drivers/available');
        return response.data;
    },
};
