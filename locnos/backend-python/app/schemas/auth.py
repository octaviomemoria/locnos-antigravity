"""
Schemas Pydantic para autenticação e tokens JWT
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import re


class Token(BaseModel):
    """Schema de resposta de tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Payload do token JWT"""
    sub: str  # user_id
    exp: Optional[int] = None


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserRegister(BaseModel):
    """Schema para registro de usuário"""
    name: str = Field(..., min_length=3, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    phone: Optional[str] = None
    document_type: str = Field(..., pattern="^(CPF|CNPJ)$")
    document_number: str = Field(..., min_length=11, max_length=18)
    
    @field_validator('document_number')
    @classmethod
    def validate_document(cls, v, info):
        """Valida CPF/CNPJ"""
        # Remove caracteres não numéricos
        digits = re.sub(r'\D', '', v)
        
        document_type = info.data.get('document_type')
        
        if document_type == 'CPF' and len(digits) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        elif document_type == 'CNPJ' and len(digits) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
            
        return digits
    
    model_config = ConfigDict(from_attributes=True)


class PasswordReset(BaseModel):
    """Schema para reset de senha"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema para confirmar reset de senha"""
    token: str
    new_password: str = Field(..., min_length=6)


class PasswordChange(BaseModel):
    """Schema para trocar senha"""
    current_password: str
    new_password: str = Field(..., min_length=6)
