"""
Router de API para Persons (Pessoas)
CRUD completo com filtros por tipo
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from uuid import UUID
from math import ceil

from app.core.database import get_db
from app.models.person import Person, PersonType, PersonStatus
from app.models.user import User
from app.schemas.person import (
    PersonCreate,
    PersonUpdate,
    PersonResponse,
    PersonListResponse
)
from app.api.deps import get_current_active_user, require_staff

router = APIRouter()


@router.get("/", response_model=PersonListResponse)
async def list_persons(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    person_type: Optional[str] = None,  # Filtrar por tipo: client, driver, employee, etc
    status: Optional[str] = None,
    defaulter_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Listar pessoas com paginação e filtros.
    
    Filtros úteis:
    - person_type="driver" → Lista apenas freteiros
    - person_type="client" → Lista apenas clientes
    - defaulter_only=true → Lista apenas inadimplentes
    """
    query = db.query(Person).filter(Person.active == True)
    
    # Busca por nome, CPF, CNPJ, email
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Person.full_name.ilike(search_filter),
                Person.company_name.ilike(search_filter),
                Person.trade_name.ilike(search_filter),
                Person.email.ilike(search_filter),
                Person.cpf.like(search.replace(".", "").replace("-", "")),
                Person.cnpj.like(search.replace(".", "").replace("/", "").replace("-", ""))
            )
        )
    
    # Filtro por tipo (usando JSONB contains)
    if person_type:
        # Verifica se o tipo está no array types
        query = query.filter(Person.types.contains([person_type]))
    
    # Filtro por status
    if status:
        query = query.filter(Person.status == status)
    
    # Filtro por inadimplentes
    if defaulter_only:
        query = query.filter(Person.defaulter == True)
    
    # Total de resultados
    total = query.count()
    
    # Paginação
    offset = (page - 1) * per_page
    items = query.order_by(Person.created_at.desc()).offset(offset).limit(per_page).all()
    
    return PersonListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=ceil(total / per_page) if total > 0 else 0
    )


@router.get("/drivers/available", response_model=List[PersonResponse])
async def list_available_drivers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Listar freteiros/motoristas disponíveis para entregas.
    
    Útil para seleção rápida ao agendar entregas/coletas.
    Retorna pessoas que têm "driver" nos types.
    """
    drivers = db.query(Person).filter(
        and_(
            Person.types.contains(["driver"]),
            Person.status == PersonStatus.APPROVED,
            Person.active == True
        )
    ).all()
    
    # Filtrar apenas os que estão disponíveis (se tiver driver_data.available)
    available_drivers = []
    for driver in drivers:
        if driver.driver_data and isinstance(driver.driver_data, dict):
            if driver.driver_data.get('available', True):  # Default true se não especificado
                available_drivers.append(driver)
        else:
            available_drivers.append(driver)  # Se não tem driver_data, assume disponível
    
    return available_drivers


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    person_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obter detalhes de uma pessoa específica"""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    
    return person


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    person_data: PersonCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Criar nova pessoa.
    
    Validações automáticas:
    - Se tipo = client: mínimo 2 referências
    - Se tipo = driver: CNH obrigatória
    - CPF/CNPJ único
    """
    # Verificar se CPF/CNPJ já existe
    if person_data.document_type == "cpf" and person_data.cpf:
        existing = db.query(Person).filter(Person.cpf == person_data.cpf).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CPF {person_data.cpf} já cadastrado"
            )
    
    if person_data.document_type == "cnpj" and person_data.cnpj:
        existing = db.query(Person).filter(Person.cnpj == person_data.cnpj).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CNPJ {person_data.cnpj} já cadastrado"
            )
    
    # Criar pessoa
    person = Person(
        **person_data.dict(exclude={'address'} if person_data.address else set()),
        address=person_data.address.dict() if person_data.address else None,
        status=PersonStatus.PENDING,  # Aguarda aprovação
        created_by_id=current_user.id
    )
    
    db.add(person)
    db.commit()
    db.refresh(person)
    
    return person


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: UUID,
    person_data: PersonUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualizar pessoa existente"""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    
    # Atualizar apenas campos fornecidos
    update_data = person_data.dict(exclude_unset=True, exclude={'address'})
    
    for field, value in update_data.items():
        setattr(person, field, value)
    
    # Atualizar endereço se fornecido
    if person_data.address:
        person.address = person_data.address.dict()
    
    person.updated_by_id = current_user.id
    
    db.commit()
    db.refresh(person)
    
    return person


@router.put("/{person_id}/approve")
async def approve_person(
    person_id: UUID,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Aprovar cadastro de pessoa.
    Requer role: staff, admin ou super_admin.
    """
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    
    from datetime import datetime
    
    person.status = PersonStatus.APPROVED
    person.approved_by_id = current_user.id
    person.approved_at = datetime.utcnow()
    
    # Se for cliente, seta customer_since
    if person.is_client and not person.customer_since:
        person.customer_since = datetime.utcnow()
    
    db.commit()
    db.refresh(person)
    
    return {"message": f"Pessoa {person.display_name} aprovada com sucesso", "person": person}


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: UUID,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    """
    Deletar pessoa (soft delete).
    Requer role: staff, admin ou super_admin.
    """
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    
    # Soft delete - apenas marca como inativo
    person.active = False
    db.commit()
    
    return None
