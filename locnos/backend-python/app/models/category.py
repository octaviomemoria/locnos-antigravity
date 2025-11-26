"""
Model SQLAlchemy para Categorias de Equipamentos
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Category(Base):
    """Model de Categoria"""
    
    __tablename__ = "categorias"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Informações básicas
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500))
    icon = Column(String(100))
    image = Column(String(500))
    
    # Hierarquia
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categorias.id"), nullable=True, index=True)
    
    # Ordenação
    order = Column(Integer, default=0, index=True)
    
    # Status
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Metadados
    total_equipment = Column(Integer, default=0)
    popularity_score = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Category {self.name}>"
