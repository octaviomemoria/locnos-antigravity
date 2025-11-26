"""
Model SQLAlchemy para Usuários (clientes, staff, admin)
Suporta multi-tenancy e roles granulares
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum, ARRAY, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """Roles de usuários"""
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(str, enum.Enum):
    """Status da conta"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    PENDING = "pending"


class DocumentType(str, enum.Enum):
    """Tipos de documento brasileiro"""
    CPF = "CPF"
    CNPJ = "CNPJ"


class User(Base):
    """Model de Usuário"""
    
    __tablename__ = "usuarios"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Informações básicas
    name = Column(String(200), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # Hash bcrypt
    
    # Role e status
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False, index=True)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False, index=True)
    
    # Contato
    phone = Column(String(20))
    whatsapp = Column(String(20))
    
    # Documento (CPF ou CNPJ)
    document_type = Column(Enum(DocumentType), nullable=False)
    document_number = Column(String(20), unique=True, nullable=False, index=True)
    document_verified = Column(Boolean, default=False)
    
    # Endereço (desnormalizado para performance)
    address_street = Column(String(200))
    address_number = Column(String(20))
    address_complement = Column(String(100))
    address_neighborhood = Column(String(100))
    address_city = Column(String(100))
    address_state = Column(String(2))
    address_zip_code = Column(String(10))
    address_country = Column(String(50), default="Brasil")
    
    # Empresa (para CNPJ)
    company_name = Column(String(200))
    company_trade_name = Column(String(200))
    company_state_registration = Column(String(50))
    company_municipal_registration = Column(String(50))
    
    # Permissões (array de strings)
    permissions = Column(ARRAY(String), default=[])
    
    # Localização/Filial
    location_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Dados do cliente
    credit_limit = Column(Numeric(10, 2), default=0)
    total_rented = Column(Integer, default=0)
    total_spent = Column(Numeric(10, 2), default=0)
    last_rental = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text)
    rating = Column(Integer, nullable=True)
    
    # Avatar
    avatar = Column(String(500))
    
    # Reset de senha
    reset_password_token = Column(String(500))
    reset_password_expire = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
    
    @property
    def is_active(self) -> bool:
        """Verifica se o usuário está ativo"""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_admin(self) -> bool:
        """Verifica se é admin ou super admin"""
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
    
    @property
    def full_address(self) -> str:
        """Retorna endereço formatado"""
        parts = [
            f"{self.address_street}, {self.address_number}" if self.address_street else None,
            self.address_complement,
            self.address_neighborhood,
            f"{self.address_city}/{self.address_state}" if self.address_city else None,
            f"CEP: {self.address_zip_code}" if self.address_zip_code else None
        ]
        return " - ".join(filter(None, parts))
