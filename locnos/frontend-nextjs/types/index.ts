// Tipos de usuários
export type UserRole = 'CUSTOMER' | 'STAFF' | 'ADMIN' | 'SUPER_ADMIN';
export type UserStatus = 'ACTIVE' | 'INACTIVE' | 'BLOCKED' | 'PENDING';

export interface User {
    id: string;
    name: string;
    email: string;
    role: UserRole;
    status: UserStatus;
    phone?: string;
    created_at: string;
}

// Auth
export interface LoginCredentials {
    email: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

// Equipamentos
export type EquipmentStatus = 'AVAILABLE' | 'RENTED' | 'MAINTENANCE' | 'UNAVAILABLE';

export interface RentalPeriod {
    description: string;
    days: number;
    value: number;
}

export interface ExternalMedia {
    type: 'video' | 'manual' | 'link';
    title: string;
    url: string;
}

export interface Equipment {
    id: string;
    name: string;
    description: string;
    brand?: string;
    category_id: string;
    subcategory_id?: string;
    internal_code: string;
    serial_number?: string;
    barcode?: string;

    // Valores
    purchase_value?: number;
    sale_value?: number;
    suggested_deposit?: number;

    // Períodos de locação flexíveis
    rental_periods: RentalPeriod[];

    // Mídia externa
    external_media?: ExternalMedia[];

    // Contrato
    contract_template?: string;
    specific_clauses?: string[];

    // Status e quantidade
    status: EquipmentStatus;
    quantity_total: number;
    quantity_available: number;
    quantity_rented: number;

    // Tags
    tags?: string[];
    visible: boolean;
    featured: boolean;

    // Relações (populadas opcionalmente)
    category?: Category;
    subcategory?: Subcategory;

    created_at: string;
    updated_at: string;
}

export interface EquipmentListResponse {
    items: Equipment[];
    total: number;
    page: number;
    per_page: number;
    pages: number;
}

// Categorias
export interface Category {
    id: string;
    name: string;
    slug: string;
    description?: string;
    icon?: string;
    active: boolean;
    total_equipment: number;
}

// Subcategorias
export interface Subcategory {
    id: string;
    nome: string;
    slug: string;
    descricao?: string;
    categoria_id: string;
    ativo: boolean;
    total_equipamentos: number;
}

// Pessoas
export type PersonType = 'CLIENT' | 'EMPLOYEE' | 'DRIVER' | 'SUPPLIER' | 'PARTNER';
export type PersonDocumentType = 'CPF' | 'CNPJ';
export type PersonStatus = 'PENDING' | 'APPROVED' | 'REJECTED';

export interface PersonReference {
    id: string;
    name: string;
    phone: string;
    relationship: string;
}

export interface DriverData {
    vehicle_type: string;
    license_plate: string;
    drivers_license: string;
    license_category: string;
    license_expiration: string;
    available: boolean;
}

export interface Person {
    id: string;
    types: string[];
    primary_type: PersonType;
    document_type: PersonDocumentType;

    // PF
    full_name?: string;
    cpf?: string;
    rg?: string;

    // PJ
    company_name?: string;
    trade_name?: string;
    cnpj?: string;

    // Contato
    email?: string;
    phone: string;
    whatsapp?: string;

    // Dados específicos
    references?: PersonReference[];
    driver_data?: DriverData;

    // Status
    status: PersonStatus;
    active: boolean;
    credit_limit: number;
    defaulter: boolean;

    created_at: string;
    updated_at: string;
}

export interface PersonListResponse {
    items: Person[];
    total: number;
    page: number;
    per_page: number;
    pages: number;
}
