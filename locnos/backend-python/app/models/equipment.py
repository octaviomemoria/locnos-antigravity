"""
Model SQLAlchemy para Equipamentos
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class EquipmentStatus(str, enum.Enum):
    """Status do equipamento"""
    AVAILABLE = "available"
    RENTED = "rented"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Equipment(Base):
    """Model de Equipamento"""
    
    __tablename__ = "equipment"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Informações básicas
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Categoria e Subcategoria
    # Categoria e Subcategoria
    category_id = Column("categoryId", UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False, index=True)
    # subcategory_id = Column("subcategoryId", UUID(as_uuid=True), ForeignKey("subcategorias.id"), nullable=True, index=True)
    
    # 🆕 NOVOS CAMPOS - Informações Expandidas
    brand = Column(String(100))  # Marca do equipamento
    
    # Códigos/Identificação
    # Códigos/Identificação
    internal_code = Column("internalCode", String(50), unique=True, nullable=False, index=True)
    serial_number = Column("serialNumber", String(100), unique=True)
    barcode = Column("barcode", String(100), unique=True, index=True)
    qr_code = Column("qrCode", String(500))
    
    # Especificações (JSON flexível)
    specifications = Column(JSONB, default={})
    
    # Imagens (array de objetos JSON)
    images = Column(JSONB, default=[])
    
    # 🆕 Valores Financeiros
    # 🆕 Valores Financeiros
    purchase_value = Column("purchaseValue", Numeric(10, 2))  # Valor de compra/aquisição
    sale_value = Column("saleValue", Numeric(10, 2))  # Valor de venda (se disponível)
    suggested_deposit = Column("suggestedDeposit", Numeric(10, 2), default=0)  # Caução sugerida
    
    # 🆕 Períodos de Locação Flexíveis (JSONB Array)
    # Substitui daily_rate, weekly_rate, monthly_rate fixos
    # 🆕 Períodos de Locação Flexíveis (JSONB Array)
    # Substitui daily_rate, weekly_rate, monthly_rate fixos
    rental_periods = Column("rentalPeriods", JSONB, default=[])
    # Exemplo:
    # [
    #   {"description": "1 a 3 dias", "days": 3, "value": 250.00},
    #   {"description": "1 semana", "days": 7, "value": 400.00},
    #   {"description": "Quinzenal", "days": 15, "value": 700.00},
    #   {"description": "Mensal", "days": 30, "value": 1200.00}
    # ]
    
    # Precificação Legada (mantida por compatibilidade, deprecated)
    # Precificação Legada (mantida por compatibilidade, deprecated)
    daily_rate = Column("dailyRate", Numeric(10, 2))  # Usar rental_periods ao invés
    weekly_rate = Column("weeklyRate", Numeric(10, 2))
    monthly_rate = Column("monthlyRate", Numeric(10, 2))
    hourly_rate = Column("hourlyRate", Numeric(10, 2))
    minimum_rental_value = Column("minimumRentalValue", Integer, default=1)
    minimum_rental_unit = Column("minimumRentalUnit", String(20), default="day")
    deposit_required = Column("depositRequired", Numeric(10, 2), default=0)  # Usar suggested_deposit
    replacement_value = Column("replacementValue", Numeric(10, 2))  # Usar sale_value
    
    # Status e quantidade
    # Status e quantidade
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.AVAILABLE, nullable=False, index=True)
    quantity_total = Column("quantityTotal", Integer, default=1, nullable=False)
    quantity_available = Column("quantityAvailable", Integer, default=1, nullable=False)
    quantity_rented = Column("quantityRented", Integer, default=0, nullable=False)
    quantity_reserved = Column("quantityReserved", Integer, default=0, nullable=False)
    quantity_maintenance = Column("quantityMaintenance", Integer, default=0, nullable=False)
    
    # Localização
    # Localização
    location_id = Column("locationId", UUID(as_uuid=True))
    current_location = Column("currentLocation", String(200))
    
    # Aquisição
    # Aquisição
    acquisition_date = Column("acquisitionDate", DateTime(timezone=True))
    acquisition_cost = Column("acquisitionCost", Numeric(10, 2))
    acquisition_supplier = Column("acquisitionSupplier", String(200))
    warranty_expiration = Column("warrantyExpiration", DateTime(timezone=True))
    warranty_description = Column("warrantyDescription", Text)
    
    # Manutenção
    # Manutenção
    last_maintenance = Column("lastMaintenance", DateTime(timezone=True))
    next_maintenance = Column("nextMaintenance", DateTime(timezone=True))
    maintenance_interval = Column("maintenanceInterval", Integer)  # dias
    total_maintenance_cost = Column("totalMaintenanceCost", Numeric(10, 2), default=0)
    
    # Estatísticas
    # Estatísticas
    total_rentals = Column("totalRentals", Integer, default=0)
    total_days_rented = Column("totalDaysRented", Integer, default=0)
    total_revenue = Column("totalRevenue", Numeric(10, 2), default=0)
    utilization_rate = Column("utilizationRate", Numeric(5, 2), default=0)
    last_rental_date = Column("lastRentalDate", DateTime(timezone=True))
    
    # Instruções (JSON ou texto)
    # Instruções (JSON ou texto)
    usage_instructions = Column("usageInstructions", Text)
    safety_instructions = Column("safetyInstructions", Text)
    maintenance_instructions = Column("maintenanceInstructions", Text)
    notes = Column(Text)
    
    # Acessórios (JSON array)
    accessories = Column(JSONB, default=[])
    
    # 🆕 Mídias Externas (Vídeos, Manuais, Links)
    # 🆕 Mídias Externas (Vídeos, Manuais, Links)
    external_media = Column("externalMedia", JSONB, default=[])
    # [
    #   {"type": "video", "title": "Como usar", "url": "https://youtube.com/..."},
    #   {"type": "manual", "title": "Manual PDF", "url": "https://..."},
    #   {"type": "link", "title": "Site fabricante", "url": "https://..."}
    # ]
    
    # 🆕 Modelo de Contrato / Cláusulas Específicas
    # 🆕 Modelo de Contrato / Cláusulas Específicas
    contract_template = Column("contractTemplate", Text)  # Template do contrato ou ID de template
    specific_clauses = Column("specificClauses", JSONB, default=[])
    # [
    #   "Equipamento deve ser devolvido limpo",
    #   "Uso exclusivo interno, proibido sublocar",
    #   "Manutenção por conta do locatário"
    # ]
    
    # Visibilidade
    visible = Column(Boolean, default=True, nullable=False)
    featured = Column(Boolean, default=False, nullable=False)
    
    # Tags para busca
    tags = Column(JSONB, default=[])
    
    # Auditoria
    # Auditoria
    created_by_id = Column("createdById", UUID(as_uuid=True))
    updated_by_id = Column("updatedById", UUID(as_uuid=True))
    created_at = Column("createdAt", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("updatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Equipment {self.name} ({self.internal_code})>"
    
    @property
    def is_available(self) -> bool:
        """Verifica se está disponível para locação"""
        return self.status == EquipmentStatus.AVAILABLE and self.quantity_available > 0
    
    @property
    def primary_image(self) -> str:
        """Retorna a URL da imagem principal"""
        if self.images and isinstance(self.images, list):
            for img in self.images:
                if isinstance(img, dict) and img.get('isPrimary'):
                    return img.get('url')
            return self.images[0].get('url') if self.images else None
        return None
