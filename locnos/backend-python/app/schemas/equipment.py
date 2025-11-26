"""
Schemas Pydantic para Equipment (request/response)  
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class RentalPeriod(BaseModel):
    """Período de locação (flexível)"""
    description: str = Field(..., min_length=3, max_length=100, description="Ex: '1 a 3 dias', '1 semana'")
    days: int = Field(..., gt=0, le=365, description="Duração em dias")
    value: Decimal = Field(..., gt=0, description="Valor total do período")


class ExternalMedia(BaseModel):
    """Mídia externa (vídeo/manual/link)"""
    type: str = Field(..., pattern="^(video|manual|link)$", description="Tipo de mídia")
    title: str = Field(..., min_length=3, max_length=200, description="Título")
    url: str = Field(..., max_length=500, description="URL do recurso")
    description: Optional[str] = None


class EquipmentBase(BaseModel):
    """Schema base de equipamento"""
    name: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    category_id: UUID
    subcategory_id: Optional[UUID] = None  # 🆕
    brand: Optional[str] = Field(None, max_length=100)  # 🆕
    
    # 🆕 Valores Financeiros
    purchase_value: Optional[Decimal] = Field(None, gt=0)
    sale_value: Optional[Decimal] = Field(None, gt=0)
    suggested_deposit: Optional[Decimal] = Field(None, ge=0)
    
    # 🆕 Períodos de Locação Flexíveis (novo sistema)
    rental_periods: List[RentalPeriod] = []
    
    # Campos legados (deprecated)
    daily_rate: Optional[Decimal] = None
    weekly_rate: Optional[Decimal] = None
    monthly_rate: Optional[Decimal] = None


class EquipmentCreate(EquipmentBase):
    """Schema para criar equipamento"""
    internal_code: str = Field(..., min_length=3, max_length=50)
    serial_number: Optional[str] = None
    barcode: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = {}
    images: Optional[List[Dict[str, Any]]] = []
    quantity_total: int = Field(default=1, ge=1)
    
    # 🆕 Mídias Externas
    external_media: Optional[List[ExternalMedia]] = []
    
    # 🆕 Contrato
    contract_template: Optional[str] = None
    specific_clauses: Optional[List[str]] = []
    
    visible: bool = True
    tags: Optional[List[str]] = []


class EquipmentUpdate(BaseModel):
    """Schema para atualizar equipamento"""
    name: Optional[str] = None
    description: Optional[str] = None
    daily_rate: Optional[Decimal] = None
    weekly_rate: Optional[Decimal] = None
    monthly_rate: Optional[Decimal] = None
    specifications: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    quantity_total: Optional[int] = None
    quantity_available: Optional[int] = None
    visible: Optional[bool] = None
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    
    model_config = ConfigDict(from_attributes=True)


class EquipmentResponse(EquipmentBase):
    """Schema de resposta de equipamento"""
    id: UUID
    internal_code: str
    status: str
    quantity_total: int
    quantity_available: int
    quantity_rented: int
    visible: bool
    featured: bool
    images: List[Dict[str, Any]] = []
    specifications: Dict[str, Any] = {}
    tags: List[str] = []
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EquipmentListResponse(BaseModel):
    """Schema para lista paginada de equipamentos"""
    items: List[EquipmentResponse]
    total: int
    page: int
    per_page: int
    pages: int


class EquipmentAvailabilityCheck(BaseModel):
    """Schema para verificar disponibilidade"""
    equipment_id: UUID
    start_date: datetime
    end_date: datetime
    quantity: int = 1


class EquipmentAvailabilityResponse(BaseModel):
    """Resposta de disponibilidade"""
    available: bool
    quantity_available: int
    estimated_price: Decimal
    rental_days: int
