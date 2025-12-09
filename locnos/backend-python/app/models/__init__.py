# Facilita imports dos models
from .user import User, UserRole, UserStatus, DocumentType
from .equipment import Equipment, EquipmentStatus
from .category import Category
from .subcategoria import Subcategoria
from .person import Person, PersonType, PersonDocumentType, PersonStatus
from .contract import Contract, ContractItem, ContractStatus

# Sistema Logística Droguista
from .pedido import Pedido, StatusPedido, TipoFrete
from .transportadora import Transportadora
from .veiculo import Veiculo, TipoVeiculo, StatusVeiculo
from .rota import Rota, TipoRota, StatusRota
# TODO: Descomentar quando implementar sistema de entregas completo
# from .comprovante_entrega import ComprovanteEntrega, StatusEntrega, TipoOcorrencia

__all__ = [
    "User", "UserRole", "UserStatus", "DocumentType",
    "Equipment", "EquipmentStatus",
    "Category",
    "Subcategoria",
    "Person", "PersonType", "PersonDocumentType", "PersonStatus",
    "Contract", "ContractItem", "ContractStatus",
    # Logística
    "Pedido", "StatusPedido", "TipoFrete",
    "Transportadora",
    "Veiculo", "TipoVeiculo", "StatusVeiculo",
    "Rota", "TipoRota", "StatusRota",
    "ComprovanteEntrega", "StatusEntrega", "TipoOcorrencia",
]

