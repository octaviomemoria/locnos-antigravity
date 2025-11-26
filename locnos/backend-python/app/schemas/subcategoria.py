"""
Schemas Pydantic para Subcategoria
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class SubcategoriaBase(BaseModel):
    """Base para Subcategoria"""
    nome: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100, pattern="^[a-z0-9-]+$")
    descricao: Optional[str] = Field(None, max_length=500)
    icone: Optional[str] = Field(None, max_length=100)
    imagem: Optional[str] = Field(None, max_length=500)
    categoria_id: UUID
    ordem: int = 0
    ativo: bool = True


class SubcategoriaCriar(SubcategoriaBase):
    """Schema para criar Subcategoria"""
    pass


class SubcategoriaAtualizar(BaseModel):
    """Schema para atualizar Subcategoria (todos campos opcionais)"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    slug: Optional[str] = Field(None, min_length=2, max_length=100, pattern="^[a-z0-9-]+$")
    descricao: Optional[str] = Field(None, max_length=500)
    icone: Optional[str] = Field(None, max_length=100)
    imagem: Optional[str] = Field(None, max_length=500)
    categoria_id: Optional[UUID] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None


class SubcategoriaResposta(SubcategoriaBase):
    """Schema para resposta de Subcategoria"""
    id: UUID
    total_equipamentos: int
    criado_em: datetime
    atualizado_em: Optional[datetime]
    
    class Config:
        from_attributes = True


class SubcategoriaListaResposta(BaseModel):
    """Schema para lista paginada de subcategorias"""
    items: List[SubcategoriaResposta]
    total: int
    page: int
    per_page: int
    pages: int
