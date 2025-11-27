from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Any

from app.api import deps
from app.models.pedido import Pedido, StatusPedido
from app.models.equipment import Equipment
from app.models.veiculo import Veiculo

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get dashboard statistics.
    """
    
    # Pedidos
    total_pedidos = db.query(func.count(Pedido.id)).scalar()
    pedidos_pendentes = db.query(func.count(Pedido.id)).filter(Pedido.status == StatusPedido.PENDENTE_EXPEDICAO).scalar()
    pedidos_em_rota = db.query(func.count(Pedido.id)).filter(Pedido.status == StatusPedido.EM_ROTA).scalar()
    
    # Equipamentos
    total_equipamentos = db.query(func.count(Equipment.id)).scalar()
    equipamentos_disponiveis = db.query(func.count(Equipment.id)).filter(Equipment.is_available == True).scalar()
    
    # Veículos
    veiculos_ativos = db.query(func.count(Veiculo.id)).filter(Veiculo.ativo == True).scalar()
    
    return {
        "orders": {
            "total": total_pedidos,
            "pending": pedidos_pendentes,
            "in_transit": pedidos_em_rota
        },
        "equipment": {
            "total": total_equipamentos,
            "available": equipamentos_disponiveis
        },
        "fleet": {
            "active_vehicles": veiculos_ativos
        }
    }
