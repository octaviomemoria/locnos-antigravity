"""
Schemas Pydantic para Person (Pessoa)
Validações específicas por tipo
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class PersonReference(BaseModel):
    """Referência pessoal"""
    id: Optional[str] = None
    name: str = Field(..., min_length=3, max_length=200, description="Nome completo")
    phone: str = Field(..., min_length=10, max_length=20, description="Telefone com DDD")
    relationship: str = Field(..., min_length=2, max_length=50, description="Parentesco/Relação")
    verified: bool = False


class PersonDocument(BaseModel):
    """Documento anexado"""
    id: Optional[str] = None
    type: str = Field(..., description="Tipo: rg_front, rg_back, cpf, cnpj, proof_address, cnh, etc")
    name: str
    url: str
    uploaded_at: Optional[datetime] = None


class PersonAddress(BaseModel):
    """Endereço"""
    cep: str = Field(..., min_length=8, max_length=9)
    street: str = Field(..., min_length=3, max_length=200, description="Logradouro")
    number: str = Field(..., max_length=20)
    complement: Optional[str] = Field(None, max_length=100)
    neighborhood: str = Field(..., min_length=2, max_length=100, description="Bairro")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="UF - 2 letras")


class EmployeeData(BaseModel):
    """Dados específicos de funcionário"""
    position: str = Field(..., min_length=2, max_length=100, description="Cargo")
    salary: Optional[Decimal] = Field(None, gt=0)
    hire_date: Optional[str] = None  # ISO date string
    department: Optional[str] = Field(None, max_length=100)
    user_id: Optional[UUID] = None  # Relacionamento com User para login


class DriverData(BaseModel):
    """Dados específicos de freteiro/motorista"""
    vehicle_type: str = Field(..., min_length=2, max_length=100, description="Tipo de veículo")
    license_plate: str = Field(..., min_length=7, max_length=8, description="Placa ABC-1234")
    drivers_license: str = Field(..., min_length=11, max_length=11, description="CNH - 11 dígitos")
    license_category: str = Field(..., pattern="^[A-E]+$", description="Categoria: A, B, C, D, E ou combinações")
    license_expiration: Optional[str] = None  # ISO date string
    available: bool = True


class SupplierData(BaseModel):
    """Dados específicos de fornecedor"""
    products: List[str] = Field(default=[], description="Produtos/serviços fornecidos")
    bank: Optional[str] = Field(None, max_length=100)
    agency: Optional[str] = Field(None, max_length=20)
    account: Optional[str] = Field(None, max_length=30)
    payment_terms: Optional[str] = Field(None, max_length=100, description="Ex: 30 dias, à vista")


class PartnerData(BaseModel):
    """Dados específicos de parceiro"""
    partnership_type: str = Field(..., max_length=100, description="Tipo de parceria")
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Porcentagem de comissão")
    contract_url: Optional[str] = None


# ============================================================================
# Schemas Principais
# ============================================================================

class PersonBase(BaseModel):
    """Base para Person"""
    types: List[str] = Field(..., min_items=1, description="Tipos: client, employee, driver, supplier, partner")
    primary_type: str = Field(default="client")
    document_type: str = Field(..., description="cpf ou cnpj")
    
    # Pessoa Física
    full_name: Optional[str] = Field(None, min_length=3, max_length=200)
    cpf: Optional[str] = Field(None, min_length=11, max_length=11)
    rg: Optional[str] = Field(None, max_length=20)
    
    # Pessoa Jurídica
    company_name: Optional[str] = Field(None, min_length=3, max_length=200, description="Razão Social")
    trade_name: Optional[str] = Field(None, max_length=200, description="Nome Fantasia")
    cnpj: Optional[str] = Field(None, min_length=14, max_length=14)
    state_registration: Optional[str] = Field(None, max_length=20)
    municipal_registration: Optional[str] = Field(None, max_length=20)
    
    # Contato
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=10, max_length=20)
    whatsapp: Optional[str] = Field(None, max_length=20)
    
    # Endereço
    address: Optional[PersonAddress] = None
    
    # Referências (obrigatório para CLIENTs)
    references: List[PersonReference] = []
    
    # Documentos
    documents: List[PersonDocument] = []
    
    # Status
    notes: Optional[str] = None
    
    # Dados específicos por tipo
    employee_data: Optional[EmployeeData] = None
    driver_data: Optional[DriverData] = None
    supplier_data: Optional[SupplierData] = None
    partner_data: Optional[PartnerData] = None


class PersonCreate(PersonBase):
    """Schema para criar Person"""
    
    @validator('types')
    def validate_types(cls, v):
        valid_types = {'client', 'employee', 'driver', 'supplier', 'partner'}
        for t in v:
            if t not in valid_types:
                raise ValueError(f"Tipo inválido: {t}. Tipos válidos: {valid_types}")
        return v
    
    @validator('full_name', always=True)
    def validate_full_name_if_cpf(cls, v, values):
        if values.get('document_type') == 'cpf' and not v:
            raise ValueError("Nome completo é obrigatório para CPF")
        return v
    
    @validator('company_name', always=True)
    def validate_company_name_if_cnpj(cls, v, values):
        if values.get('document_type') == 'cnpj' and not v:
            raise ValueError("Razão Social é obrigatória para CNPJ")
        return v
    
    @validator('references', always=True)
    def validate_references_for_clients(cls, v, values):
        types = values.get('types', [])
        if 'client' in types:
            # Clientes precisam de mínimo 2 referências
            valid_refs = [r for r in v if r.name and r.phone and r.relationship]
            if len(valid_refs) < 2:
                raise ValueError("Clientes precisam de pelo menos 2 referências pessoais completas")
        return v
    
    @validator('driver_data', always=True)
    def validate_driver_data(cls, v, values):
        types = values.get('types', [])
        if 'driver' in types and not v:
            raise ValueError("Freteiros precisam informar dados do veículo e CNH")
        return v


class PersonUpdate(BaseModel):
    """Schema para atualizar Person (todos campos opcionais)"""
    types: Optional[List[str]] = None
    primary_type: Optional[str] = None
    
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    
    company_name: Optional[str] = None
    trade_name: Optional[str] = None
    cnpj: Optional[str] = None
    state_registration: Optional[str] = None
    municipal_registration: Optional[str] = None
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    
    address: Optional[PersonAddress] = None
    references: Optional[List[PersonReference]] = None
    documents: Optional[List[PersonDocument]] = None
    
    notes: Optional[str] = None
    
    employee_data: Optional[EmployeeData] = None
    driver_data: Optional[DriverData] = None
    supplier_data: Optional[SupplierData] = None
    partner_data: Optional[PartnerData] = None
    
    defaulter: Optional[bool] = None
    credit_limit: Optional[Decimal] = None


class PersonResponse(PersonBase):
    """Schema para resposta de Person"""
    id: UUID
    status: str
    active: bool
    
    # Financeiro
    credit_limit: Decimal
    defaulter: bool
    total_rentals: int
    total_spent: Decimal
    
    # Approval
    approved_by_id: Optional[UUID]
    approved_at: Optional[datetime]
    
    # Audit
    created_by_id: Optional[UUID]
    updated_by_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    customer_since: Optional[datetime]
    
    class Config:
        from_attributes = True


class PersonListResponse(BaseModel):
    """Schema para lista paginada de persons"""
    items: List[PersonResponse]
    total: int
    page: int
    per_page: int
    pages: int
