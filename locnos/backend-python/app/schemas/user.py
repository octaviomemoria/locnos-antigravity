"""
Schemas Pydantic para User (request/response)
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Schema base de usuário"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    document_type: str
    document_number: str


class UserCreate(UserBase):
    """Schema para criar usuário"""
    password: str = Field(..., min_length=6)
    role: Optional[str] = "customer"


class UserUpdate(BaseModel):
    """Schema para atualizar usuário"""
    name: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zip_code: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """Schema de resposta de usuário"""
    id: UUID
    role: str
    status: str
    document_verified: bool
    created_at: datetime
    avatar: Optional[str] = None
    
    # Dados do cliente
    credit_limit: Optional[float] = None
    total_rented: Optional[int] = None
    total_spent: Optional[float] = None
    rating: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserMe(UserResponse):
    """Schema completo do usuário autenticado"""
    permissions: List[str] = []
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
