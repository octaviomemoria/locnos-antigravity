"""
API Endpoints para Contratos de Locação
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal

from app.core.database import get_db
from app.api.deps import get_current_user, require_permission
from app.models import Contract, ContractItem, ContractStatus, User, Person, Equipment
from app.schemas.contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractListResponse,
    ContractListItem,
    ContractStatusUpdate,
    ContractItemCreate,
    ContractItemResponse,
    ContractCalculation,
    ContractFilters
)

router = APIRouter()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_contract_number(db: Session) -> str:
    """
    Gera número único de contrato no formato: CON-YYYY-NNNN
    Exemplo: CON-2024-0001
    """
    year = datetime.now().year
    prefix = f"CON-{year}-"
    
    # Buscar último contrato do ano
    last_contract = db.query(Contract).filter(
        Contract.contract_number.like(f"{prefix}%")
    ).order_by(Contract.contract_number.desc()).first()
    
    if last_contract:
        # Extrair número e incrementar
        last_number = int(last_contract.contract_number.split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f"{prefix}{new_number:04d}"


def calculate_contract_totals(start_date: date, end_date: date, items: List[ContractItem]) -> tuple[int, Decimal]:
    """
    Calcula total de dias e valor total do contrato
    
    Returns:
        tuple: (total_days, total_value)
    """
    total_days = (end_date - start_date).days + 1  # +1 para incluir o último dia
    total_value = Decimal(0)
    
    for item in items:
        item_subtotal = item.daily_rate * item.quantity * total_days
        item.subtotal = item_subtotal
        total_value += item_subtotal
    
    return total_days, total_value


def check_equipment_availability(
    db: Session,
    equipment_id: str,
    start_date: date,
    end_date: date,
    exclude_contract_id: Optional[str] = None
) -> bool:
    """
    Verifica se equipamento está disponível no período
    
    Args:
        db: Sessão do banco
        equipment_id: ID do equipamento
        start_date: Data de início
        end_date: Data de término
        exclude_contract_id: ID do contrato a excluir da verificação (para edição)
    
    Returns:
        bool: True se disponível, False caso contrário
    """
    # Buscar contratos ativos que conflitam com o período
    query = db.query(Contract).join(ContractItem).filter(
        and_(
            ContractItem.equipment_id == equipment_id,
            Contract.status.in_([ContractStatus.APROVADO, ContractStatus.ATIVO]),
            Contract.deleted_at.is_(None),
            or_(
                # Período solicitado sobrepõe início de contrato existente
                and_(Contract.start_date <= start_date, Contract.end_date >= start_date),
                # Período solicitado sobrepõe fim de contrato existente
                and_(Contract.start_date <= end_date, Contract.end_date >= end_date),
                # Período solicitado contém contrato existente
                and_(Contract.start_date >= start_date, Contract.end_date <= end_date)
            )
        )
    )
    
    if exclude_contract_id:
        query = query.filter(Contract.id != exclude_contract_id)
    
    conflicting_contracts = query.count()
    return conflicting_contracts == 0


def validate_status_transition(current_status: ContractStatus, new_status: ContractStatus) -> bool:
    """
    Valida se transição de status é permitida
    
    Fluxo permitido:
    - RASCUNHO -> AGUARDANDO_APROVACAO
    - AGUARDANDO_APROVACAO -> APROVADO ou RASCUNHO
    - APROVADO -> ATIVO
    - ATIVO -> FINALIZADO
    - Qualquer -> CANCELADO (exceto FINALIZADO)
    """
    valid_transitions = {
        ContractStatus.RASCUNHO: [ContractStatus.AGUARDANDO_APROVACAO, ContractStatus.CANCELADO],
        ContractStatus.AGUARDANDO_APROVACAO: [ContractStatus.APROVADO, ContractStatus.RASCUNHO, ContractStatus.CANCELADO],
        ContractStatus.APROVADO: [ContractStatus.ATIVO, ContractStatus.CANCELADO],
        ContractStatus.ATIVO: [ContractStatus.FINALIZADO, ContractStatus.CANCELADO],
        ContractStatus.FINALIZADO: [],  # Estado final
        ContractStatus.CANCELADO: []  # Estado final
    }
    
    return new_status in valid_transitions.get(current_status, [])


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=ContractListResponse)
async def list_contracts(
    status: Optional[ContractStatus] = None,
    customer_id: Optional[str] = None,
    start_date_from: Optional[date] = None,
    start_date_to: Optional[date] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar contratos com filtros e paginação
    
    - **status**: Filtrar por status
    - **customer_id**: Filtrar por cliente
    - **start_date_from/to**: Filtrar por período de início
    - **search**: Buscar por número de contrato ou nome do cliente
    """
    # Base query
    query = db.query(Contract).filter(Contract.deleted_at.is_(None))
    
    # Aplicar filtros
    if status:
        query = query.filter(Contract.status == status)
    
    if customer_id:
        query = query.filter(Contract.customer_id == customer_id)
    
    if start_date_from:
        query = query.filter(Contract.start_date >= start_date_from)
    
    if start_date_to:
        query = query.filter(Contract.start_date <= start_date_to)
    
    if search:
        query = query.join(Person, Contract.customer_id == Person.id).filter(
            or_(
                Contract.contract_number.ilike(f"%{search}%"),
                Person.name.ilike(f"%{search}%")
            )
        )
    
    # Contar total
    total = query.count()
    
    # Paginação
    offset = (page - 1) * page_size
    contracts = query.options(
        joinedload(Contract.customer),
        joinedload(Contract.items)
    ).order_by(Contract.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Montar resposta
    items = [
        ContractListItem(
            id=contract.id,
            contract_number=contract.contract_number,
            customer_name=contract.customer.name,
            status=contract.status,
            start_date=contract.start_date,
            end_date=contract.end_date,
            total_value=contract.total_value,
            total_days=contract.total_days,
            items_count=len(contract.items),
            created_at=contract.created_at
        )
        for contract in contracts
    ]
    
    total_pages = (total + page_size - 1) // page_size
    
    return ContractListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract_data: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Criar novo contrato
    
    - Valida disponibilidade dos equipamentos
    - Calcula automaticamente valores e dias
    - Gera número único de contrato
    """
    # Validar que cliente existe
    customer = db.query(Person).filter(Person.id == contract_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    # Validar disponibilidade de cada equipamento
    for item in contract_data.items:
        equipment = db.query(Equipment).filter(Equipment.id == item.equipment_id).first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipamento {item.equipment_id} não encontrado"
            )
        
        if not check_equipment_availability(
            db, item.equipment_id, contract_data.start_date, contract_data.end_date
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Equipamento '{equipment.name}' não está disponível no período solicitado"
            )
    
    # Criar contrato
    contract = Contract(
        contract_number=generate_contract_number(db),
        customer_id=contract_data.customer_id,
        created_by_id=current_user.id,
        start_date=contract_data.start_date,
        end_date=contract_data.end_date,
        notes=contract_data.notes,
        status=ContractStatus.RASCUNHO
    )
    
    # Criar itens
    contract_items = []
    for item_data in contract_data.items:
        item = ContractItem(
            equipment_id=item_data.equipment_id,
            quantity=item_data.quantity,
            daily_rate=item_data.daily_rate,
            notes=item_data.notes
        )
        contract_items.append(item)
    
    contract.items = contract_items
    
    # Calcular totais
    total_days, total_value = calculate_contract_totals(
        contract.start_date, contract.end_date, contract.items
    )
    contract.total_days = total_days
    contract.total_value = total_value
    
    # Salvar
    db.add(contract)
    db.commit()
    db.refresh(contract)
    
    # Retornar resposta
    return _build_contract_response(contract)


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter detalhes de um contrato"""
    contract = db.query(Contract).options(
        joinedload(Contract.customer),
        joinedload(Contract.created_by),
        joinedload(Contract.approved_by),
        joinedload(Contract.items).joinedload(ContractItem.equipment)
    ).filter(
        Contract.id == contract_id,
        Contract.deleted_at.is_(None)
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    return _build_contract_response(contract)


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: str,
    contract_data: ContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("contracts:update"))
):
    """
    Atualizar contrato (apenas rascunhos ou aguardando aprovação)
    """
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.deleted_at.is_(None)
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    if not contract.can_be_edited:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contrato no status '{contract.status.value}' não pode ser editado"
        )
    
    # Atualizar campos
    if contract_data.start_date:
        contract.start_date = contract_data.start_date
    if contract_data.end_date:
        contract.end_date = contract_data.end_date
    if contract_data.notes is not None:
        contract.notes = contract_data.notes
    
    # Recalcular totais se datas mudaram
    if contract_data.start_date or contract_data.end_date:
        total_days, total_value = calculate_contract_totals(
            contract.start_date, contract.end_date, contract.items
        )
        contract.total_days = total_days
        contract.total_value = total_value
    
    db.commit()
    db.refresh(contract)
    
    return _build_contract_response(contract)


@router.put("/{contract_id}/status", response_model=ContractResponse)
async def update_contract_status(
    contract_id: str,
    status_data: ContractStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("contracts:approve"))
):
    """
    Atualizar status do contrato (workflow)
    
    Requer permissão de staff+ para aprovar
    """
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.deleted_at.is_(None)
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    # Validar transição
    if not validate_status_transition(contract.status, status_data.status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transição de '{contract.status.value}' para '{status_data.status.value}' não é permitida"
        )
    
    # Atualizar status
    old_status = contract.status
    contract.status = status_data.status
    
    # Atualizar timestamps específicos
    now = datetime.utcnow()
    if status_data.status == ContractStatus.APROVADO:
        contract.approved_at = now
        contract.approved_by_id = current_user.id
    elif status_data.status == ContractStatus.ATIVO:
        contract.activated_at = now
    elif status_data.status == ContractStatus.FINALIZADO:
        contract.finished_at = now
    elif status_data.status == ContractStatus.CANCELADO:
        contract.cancelled_at = now
        contract.cancellation_reason = status_data.cancellation_reason
    
    # Adicionar nota se fornecida
    if status_data.notes:
        if contract.notes:
            contract.notes += f"\n\n[{now.strftime('%d/%m/%Y %H:%M')}] {status_data.notes}"
        else:
            contract.notes = f"[{now.strftime('%d/%m/%Y %H:%M')}] {status_data.notes}"
    
    db.commit()
    db.refresh(contract)
    
    return _build_contract_response(contract)


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
    contract_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("contracts:delete"))
):
    """
    Deletar contrato (soft delete)
    
    Apenas contratos em rascunho podem ser deletados
    """
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.deleted_at.is_(None)
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    
    if contract.status != ContractStatus.RASCUNHO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas contratos em rascunho podem ser deletados"
        )
    
    contract.deleted_at = datetime.utcnow()
    db.commit()
    
    return None


# ============================================================================
# HELPER PARA MONTAR RESPOSTA
# ============================================================================

def _build_contract_response(contract: Contract) -> ContractResponse:
    """Monta resposta completa do contrato"""
    return ContractResponse(
        id=contract.id,
        contract_number=contract.contract_number,
        customer_id=contract.customer_id,
        customer_name=contract.customer.name,
        start_date=contract.start_date,
        end_date=contract.end_date,
        status=contract.status,
        total_value=contract.total_value,
        total_days=contract.total_days,
        notes=contract.notes,
        cancellation_reason=contract.cancellation_reason,
        created_by_name=contract.created_by.name,
        approved_by_name=contract.approved_by.name if contract.approved_by else None,
        items=[
            ContractItemResponse(
                id=item.id,
                contract_id=item.contract_id,
                equipment_id=item.equipment_id,
                equipment_name=item.equipment.name,
                quantity=item.quantity,
                daily_rate=item.daily_rate,
                subtotal=item.subtotal,
                notes=item.notes,
                created_at=item.created_at,
                updated_at=item.updated_at
            )
            for item in contract.items
        ],
        created_at=contract.created_at,
        updated_at=contract.updated_at,
        approved_at=contract.approved_at,
        activated_at=contract.activated_at,
        finished_at=contract.finished_at,
        cancelled_at=contract.cancelled_at
    )
