import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { personService } from '@/lib/api/person';

export function usePersons(params?: {
    page?: number;
    per_page?: number;
    search?: string;
    person_type?: string;
    status?: string;
}) {
    return useQuery({
        queryKey: ['persons', params],
        queryFn: () => personService.getAll(params),
    });
}

export function usePersonById(id: string) {
    return useQuery({
        queryKey: ['person', id],
        queryFn: () => personService.getById(id),
        enabled: !!id,
    });
}

export function useCreatePerson() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: personService.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['persons'] });
        },
    });
}

export function useUpdatePerson() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: any }) =>
            personService.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['persons'] });
            queryClient.invalidateQueries({ queryKey: ['person'] });
        },
    });
}

export function useDeletePerson() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: personService.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['persons'] });
        },
    });
}
