"""
Schemas Pydantic para Contratos de Locação
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from app.models.contract import ContractStatus


# ============================================================================
# CONTRACT ITEM SCHEMAS
# ============================================================================

class ContractItemBase(BaseModel):
    """Schema base para item de contrato"""
    equipment_id: str = Field(..., description="ID do equipamento")
    quantity: int = Field(ge=1, description="Quantidade de equipamentos")
    daily_rate: Decimal = Field(ge=0, description="Valor da diária")
    notes: Optional[str] = Field(None, description="Observações sobre o item")


class ContractItemCreate(ContractItemBase):
    """Schema para criar item de contrato"""
    pass


class ContractItemUpdate(BaseModel):
    """Schema para atualizar item de contrato"""
    quantity: Optional[int] = Field(None, ge=1)
    daily_rate: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class ContractItemResponse(ContractItemBase):
    """Schema de resposta de item de contrato"""
    id: str
    contract_id: str
    equipment_name: str
    subtotal: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# CONTRACT SCHEMAS
# ============================================================================

class ContractBase(BaseModel):
    """Schema base para contrato"""
    customer_id: str = Field(..., description="ID do cliente")
    start_date: date = Field(..., description="Data de início do contrato")
    end_date: date = Field(..., description="Data de término do contrato")
    notes: Optional[str] = Field(None, description="Observações gerais")
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: date, info) -> date:
        """Valida que data de término é após data de início"""
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError('Data de término deve ser posterior à data de início')
        return v


class ContractCreate(ContractBase):
    """Schema para criar contrato"""
    items: List[ContractItemCreate] = Field(..., min_length=1, description="Itens do contrato")
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v: List[ContractItemCreate]) -> List[ContractItemCreate]:
        """Valida que há pelo menos um item"""
        if not v or len(v) == 0:
            raise ValueError('Contrato deve ter pelo menos um item')
        return v


class ContractUpdate(BaseModel):
    """Schema para atualizar contrato (apenas campos editáveis)"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """Valida que data de término é após data de início"""
        if v and 'start_date' in info.data and info.data['start_date']:
            if v <= info.data['start_date']:
                raise ValueError('Data de término deve ser posterior à data de início')
        return v


class ContractStatusUpdate(BaseModel):
    """Schema para atualizar status do contrato"""
    status: ContractStatus = Field(..., description="Novo status do contrato")
    notes: Optional[str] = Field(None, description="Motivo da mudança de status")
    cancellation_reason: Optional[str] = Field(None, description="Motivo do cancelamento (se aplicável)")


class ContractResponse(ContractBase):
    """Schema de resposta completa de contrato"""
    id: str
    contract_number: str
    status: ContractStatus
    total_value: Decimal
    total_days: int
    
    # Informações de relacionamentos
    customer_name: str
    created_by_name: str
    approved_by_name: Optional[str] = None
    
    # Items do contrato
    items: List[ContractItemResponse] = []
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    activated_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    # Observações
    cancellation_reason: Optional[str] = None
    
    class Config:
        from_attributes = True


class ContractListItem(BaseModel):
    """Schema simplificado para listagem de contratos"""
    id: str
    contract_number: str
    customer_name: str
    status: ContractStatus
    start_date: date
    end_date: date
    total_value: Decimal
    total_days: int
    items_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractListResponse(BaseModel):
    """Schema de resposta paginada para listagem"""
    items: List[ContractListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class ContractCalculation(BaseModel):
    """Schema para cálculo de valores do contrato"""
    total_days: int
    total_value: Decimal
    items: List[dict]  # Lista com cálculo de cada item


# ============================================================================
# FILTER SCHEMAS
# ============================================================================

class ContractFilters(BaseModel):
    """Schema para filtros de busca de contratos"""
    status: Optional[ContractStatus] = None
    customer_id: Optional[str] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    search: Optional[str] = None  # Busca por número ou nome do cliente
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
