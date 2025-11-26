import * as z from 'zod';

// Equipment validations
export const equipmentSchema = z.object({
    name: z.string().min(3, 'Nome deve ter no mínimo 3 caracteres'),
    brand: z.string().optional(),
    description: z.string().optional(),
    category_id: z.string().uuid('Selecione uma categoria válida'),
    internal_code: z.string().min(1, 'Código interno é obrigatório'),
    quantity_total: z.number().min(1, 'Quantidade deve ser maior que 0'),
    rental_value: z.number().min(0, 'Valor deve ser maior ou igual a 0').optional(),
    status: z.enum(['AVAILABLE', 'RENTED', 'MAINTENANCE', 'UNAVAILABLE']).default('AVAILABLE'),
});

export type EquipmentFormData = z.infer<typeof equipmentSchema>;

// Person validations
export const personSchema = z.object({
    types: z.array(z.string()).min(1, 'Selecione pelo menos um tipo'),
    document_type: z.enum(['CPF', 'CNPJ']),
    full_name: z.string().optional(),
    company_name: z.string().optional(),
    cpf: z.string().optional(),
    cnpj: z.string().optional(),
    phone: z.string().min(10, 'Telefone inválido'),
    email: z.string().email('E-mail inválido').optional(),
    status: z.enum(['PENDING', 'APPROVED', 'REJECTED']).default('PENDING'),
});

export type PersonFormData = z.infer<typeof personSchema>;
