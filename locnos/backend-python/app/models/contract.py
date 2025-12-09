"""
Models SQLAlchemy para Contratos de Locação
"""

from sqlalchemy import Column, String, DateTime, Numeric, Integer, ForeignKey, Enum as SQLEnum, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base
import uuid


class ContractStatus(str, enum.Enum):
    """Status possíveis de um contrato"""
    RASCUNHO = "rascunho"
    AGUARDANDO_APROVACAO = "aguardando_aprovacao"
    APROVADO = "aprovado"
    ATIVO = "ativo"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class Contract(Base):
    """
    Model de Contrato de Locação
    
    Representa um contrato entre a locadora e um cliente para locação de equipamentos.
    """
    __tablename__ = "contratos"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_number = Column(String, unique=True, nullable=False, index=True)  # Auto-gerado: CON-2024-0001
    
    # Relacionamentos (Foreign Keys)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"), nullable=False, index=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    approved_by_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    
    # Datas do contrato
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Status e valores calculados
    status = Column(SQLEnum(ContractStatus), default=ContractStatus.RASCUNHO, nullable=False, index=True)
    total_value = Column(Numeric(10, 2), default=0, nullable=False)
    total_days = Column(Integer, default=0, nullable=False)
    
    # Observações e notas
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Timestamps de auditoria
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    activated_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships (ORM)
    customer = relationship("Person", foreign_keys=[customer_id], backref="contracts")
    created_by = relationship("User", foreign_keys=[created_by_id], backref="created_contracts")
    approved_by = relationship("User", foreign_keys=[approved_by_id], backref="approved_contracts")
    items = relationship("ContractItem", back_populates="contract", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Contract {self.contract_number} - {self.status.value}>"
    
    @property
    def is_active(self):
        """Verifica se o contrato está ativo"""
        return self.status == ContractStatus.ATIVO and self.deleted_at is None
    
    @property
    def can_be_edited(self):
        """Verifica se o contrato pode ser editado"""
        return self.status in [ContractStatus.RASCUNHO, ContractStatus.AGUARDANDO_APROVACAO]
    
    @property
    def can_be_approved(self):
        """Verifica se o contrato pode ser aprovado"""
        return self.status == ContractStatus.AGUARDANDO_APROVACAO
    
    @property
    def can_be_activated(self):
        """Verifica se o contrato pode ser ativado"""
        return self.status == ContractStatus.APROVADO
    
    @property
    def can_be_cancelled(self):
        """Verifica se o contrato pode ser cancelado"""
        return self.status in [
            ContractStatus.RASCUNHO,
            ContractStatus.AGUARDANDO_APROVACAO,
            ContractStatus.APROVADO,
            ContractStatus.ATIVO
        ]


class ContractItem(Base):
    """
    Model de Item do Contrato
    
    Representa um equipamento incluído em um contrato de locação.
    """
    __tablename__ = "itens_contrato"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relacionamentos (Foreign Keys)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contratos.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipamentos.id"), nullable=False, index=True)
    
    # Quantidade e valores
    quantity = Column(Integer, nullable=False, default=1)
    daily_rate = Column(Numeric(10, 2), nullable=False)  # Diária no momento do contrato (histórico)
    subtotal = Column(Numeric(10, 2), nullable=False, default=0)  # Calculado: daily_rate * quantity * days
    
    # Observações específicas do item
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships (ORM)
    contract = relationship("Contract", back_populates="items")
    equipment = relationship("Equipment", backref="contract_items")
    
    def __repr__(self):
        return f"<ContractItem {self.equipment_id} x{self.quantity}>"
    
    def calculate_subtotal(self, total_days: int):
        """
        Calcula o subtotal do item
        
        Args:
            total_days: Número total de dias do contrato
            
        Returns:
            Decimal: Subtotal calculado
        """
        return self.daily_rate * self.quantity * total_days
