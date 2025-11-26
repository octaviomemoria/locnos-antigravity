"""
Router API para Subcategorias
CRUD completo
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from uuid import UUID
from math import ceil

from app.core.database import get_db
from app.models.subcategoria import Subcategoria
from app.models.user import User
from app.schemas.subcategoria import (
    SubcategoriaCriar,
    SubcategoriaAtualizar,
    SubcategoriaResposta,
    SubcategoriaListaResposta
)
from app.api.deps import get_current_active_user, require_staff

router = APIRouter()


@router.get("/", response_model=SubcategoriaListaResposta)
async def listar_subcategorias(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    categoria_id: Optional[UUID] = None,
    ativo_apenas: bool = True,
    db: Session = Depends(get_db)
):
    """
    Listar subcategorias com paginação.
    Endpoint público.
    """
    query = db.query(Subcategoria)
    
    # Filtro por categoria pai
    if categoria_id:
        query = query.filter(Subcategoria.categoria_id == categoria_id)
    
    # Filtro por ativas
    if ativo_apenas:
        query = query.filter(Subcategoria.ativo == True)
    
    # Total
    total = query.count()
    
    # Ordenar por ordem e nome
    query = query.order_by(Subcategoria.ordem, Subcategoria.nome)
    
    # Paginação
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()
    
    return SubcategoriaListaResposta(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=ceil(total / per_page) if total > 0 else 0
    )


@router.get("/{subcategoria_id}", response_model=SubcategoriaResposta)
async def obter_subcategoria(
    subcategoria_id: UUID,
    db: Session = Depends(get_db)
):
    """Obter detalhes de uma subcategoria"""
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id == subcategoria_id).first()
    
    if not subcategoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategoria não encontrada"
        )
    
    return subcategoria


@router.post("/", response_model=SubcategoriaResposta, status_code=status.HTTP_201_CREATED)
async def criar_subcategoria(
    subcategoria_data: SubcategoriaCriar,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Criar nova subcategoria.
    Requer role: staff, admin ou super_admin.
    """
    # Verificar se slug já existe
    existing = db.query(Subcategoria).filter(Subcategoria.slug == subcategoria_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slug '{subcategoria_data.slug}' já existe"
        )
    
    # Criar subcategoria
    subcategoria = Subcategoria(**subcategoria_data.dict())
    
    db.add(subcategoria)
    db.commit()
    db.refresh(subcategoria)
    
    return subcategoria


@router.put("/{subcategoria_id}", response_model=SubcategoriaResposta)
async def atualizar_subcategoria(
    subcategoria_id: UUID,
    subcategoria_data: SubcategoriaAtualizar,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Atualizar subcategoria.
    Requer role: staff, admin ou super_admin.
    """
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id == subcategoria_id).first()
    
    if not subcategoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategoria não encontrada"
        )
    
    # Atualizar campos fornecidos
    update_data = subcategoria_data.dict(exclude_unset=True)
    
    # Verificar slug único se foi alterado
    if 'slug' in update_data and update_data['slug'] != subcategoria.slug:
        existing = db.query(Subcategoria).filter(Subcategoria.slug == update_data['slug']).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slug '{update_data['slug']}' já existe"
            )
    
    for field, value in update_data.items():
        setattr(subcategoria, field, value)
    
    db.commit()
    db.refresh(subcategoria)
    
    return subcategoria


@router.delete("/{subcategoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_subcategoria(
    subcategoria_id: UUID,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Deletar subcategoria.
    Requer role: staff, admin ou super_admin.
    """
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id == subcategoria_id).first()
    
    if not subcategoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategoria não encontrada"
        )
    
    # Verificar se tem equipamentos associados
    if subcategoria.total_equipamentos and subcategoria.total_equipamentos > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar. Existem {subcategoria.total_equipamentos} equipamentos nesta subcategoria."
        )
    
    db.delete(subcategoria)
    db.commit()
    
    return None
