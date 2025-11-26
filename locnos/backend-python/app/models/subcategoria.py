"""
Model SQLAlchemy para Subcategorias
Hierarquia: Categoria > Subcategoria > Equipamento
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Subcategoria(Base):
    """Model de Subcategoria de Equipamentos"""
    
    __tablename__ = "subcategorias"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Informações básicas
    nome = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(String(500))
    icone = Column(String(100))
    imagem = Column(String(500))
    
    # Relacionamento com categoria pai
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias.id"), nullable=False, index=True)
    
    # Ordenação e visibilidade
    ordem = Column(Integer, default=0, index=True)
    ativo = Column(Boolean, default=True, nullable=False, index=True)
    
    # Metadados
    total_equipamentos = Column(Integer, default=0)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Subcategoria {self.nome}>"
