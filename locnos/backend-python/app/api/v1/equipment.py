"""
Router de Equipamentos - CRUD completo + busca/filtros
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from uuid import UUID
from math import ceil

from app.core.database import get_db
from app.models.equipment import Equipment, EquipmentStatus
from app.models.user import User
from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
    EquipmentListResponse
)
from app.api.deps import get_current_active_user, require_staff

router = APIRouter()


@router.get("/", response_model=EquipmentListResponse)
async def list_equipment(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[UUID] = None,
    status: Optional[EquipmentStatus] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Listar equipamentos com paginação e filtros.
    Endpoint público (não requer autenticação).
    """
    query = db.query(Equipment)
    
    # Filtros
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Equipment.name.ilike(search_filter),
                Equipment.description.ilike(search_filter),
                Equipment.internal_code.ilike(search_filter)
            )
        )
    
    if category_id:
        query = query.filter(Equipment.category_id == category_id)
    
    if status:
        query = query.filter(Equipment.status == status)
    
    if min_price:
        query = query.filter(Equipment.daily_rate >= min_price)
    
    if max_price:
        query = query.filter(Equipment.daily_rate <= max_price)
    
    if available_only:
        query = query.filter(
            Equipment.status == EquipmentStatus.AVAILABLE,
            Equipment.quantity_available > 0,
            Equipment.visible == True
        )
    
    # Apenas equipamentos visíveis por padrão
    query = query.filter(Equipment.visible == True)
    
    # Total de resultados
    total = query.count()
    
    # Paginação
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()
    
    return EquipmentListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=ceil(total / per_page) if total > 0 else 0
    )


@router.get("/{equipment_id}", response_model=EquipmentResponse)
async def get_equipment(
    equipment_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Obter detalhes de um equipamento específico.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado"
        )
    
    return equipment


@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    equipment_data: EquipmentCreate,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Criar novo equipamento.
    Requer role: staff, admin ou super_admin.
    """
    # Verificar se internal_code já existe
    existing = db.query(Equipment).filter(
        Equipment.internal_code == equipment_data.internal_code
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Código interno '{equipment_data.internal_code}' já existe"
        )
    
    # Criar equipamento
    equipment = Equipment(
        **equipment_data.model_dump(),
        quantity_available=equipment_data.quantity_total,
        status=EquipmentStatus.AVAILABLE,
        created_by_id=current_user.id
    )
    
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
async def update_equipment(
    equipment_id: UUID,
    equipment_data: EquipmentUpdate,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Atualizar equipamento existente.
    Requer role: staff, admin ou super_admin.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado"
        )
    
    # Atualizar apenas campos fornecidos
    update_data = equipment_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(equipment, field, value)
    
    equipment.updated_by_id = current_user.id
    
    db.commit()
    db.refresh(equipment)
    
    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(
    equipment_id: UUID,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Deletar equipamento.
    Requer role: staff, admin ou super_admin.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipamento não encontrado"
        )
    
    # Soft delete - apenas marca como invisível
    equipment.visible = False
    db.commit()
    
    return None
