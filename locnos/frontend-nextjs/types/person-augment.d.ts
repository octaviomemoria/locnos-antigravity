// Force TypeScript to recognize Person type with all fields
// This file ensures Vercel build recognizes all Person properties

import { Person as BasePerson } from './types';

declare module './types' {
    export interface Person extends Omit<BasePerson, never> {
        // Força reconhecimento de todos os campos
        notes?: string;
        documents?: any;
        employee_data?: any;
        supplier_data?: any;
        partner_data?: any;
        total_rentals?: number;
        total_spent?: number;
        customer_since?: string;
    }
}
