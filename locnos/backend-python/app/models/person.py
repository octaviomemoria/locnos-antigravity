"""
Model SQLAlchemy para Pessoas (Unified Person Registry)
Substitui o conceito de "Cliente" por "Pessoa" com múltiplos tipos
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class PersonType(str, enum.Enum):
    """Tipos de pessoa no sistema (extensível)"""
    CLIENT = "client"           # Cliente - aluga equipamentos
    EMPLOYEE = "employee"       # Funcionário da organização
    DRIVER = "driver"           # Freteiro - faz entregas/coletas
    SUPPLIER = "supplier"       # Fornecedor de equipamentos
    PARTNER = "partner"         # Parceiro comercial
    # Admin pode adicionar novos tipos via configuração


class PersonDocumentType(str, enum.Enum):
    """Tipo de documento (PF ou PJ)"""
    CPF = "cpf"   # Pessoa Física
    CNPJ = "cnpj"  # Pessoa Jurídica


class PersonStatus(str, enum.Enum):
    """Status do cadastro da pessoa"""
    PENDING = "pending"      # Aguardando aprovação
    APPROVED = "approved"    # Aprovado e ativo
    BLOCKED = "blocked"      # Bloqueado (inadimplência, etc)
    INACTIVE = "inactive"    # Inativo


class Person(Base):
    """
    Model de Pessoa Unificado
    
    Uma pessoa pode ter múltiplos tipos simultaneamente.
    Exemplo: João pode ser CLIENT + DRIVER (aluga equipamentos e faz entregas)
    """
    
    __tablename__ = "pessoas"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Tipos (ARRAY - pode ter múltiplos!)
    # Exemplo: ["client", "driver"]
    types = Column(JSONB, default=[], nullable=False)
    primary_type = Column(Enum(PersonType), default=PersonType.CLIENT, nullable=False, index=True)
    
    # Informações Básicas
    document_type = Column(Enum(PersonDocumentType), nullable=False)
    
    # Pessoa Física (CPF)
    full_name = Column(String(200), index=True)
    cpf = Column(String(11), unique=True, index=True)
    rg = Column(String(20))
    
    # Pessoa Jurídica (CNPJ)
    company_name = Column(String(200))      # Razão Social
    trade_name = Column(String(200))        # Nome Fantasia
    cnpj = Column(String(14), unique=True, index=True)
    state_registration = Column(String(20))  # Inscrição Estadual
    municipal_registration = Column(String(20))  # Inscrição Municipal
    
    # Contato
    email = Column(String(255), index=True)
    phone = Column(String(20), nullable=False)
    whatsapp = Column(String(20))
    
    # Endereço (JSON com integração ViaCEP
    address = Column(JSONB)
    # {
    #   "cep": "01310-100",
    #   "street": "Av Paulista",
    #   "number": "1578",
    #   "complement": "Sala 10",
    #   "neighborhood": "Bela Vista",
    #   "city": "São Paulo",
    #   "state": "SP"
    # }
    
    # Referências Pessoais (OBRIGATÓRIO para tipo CLIENT - mínimo 2)
    references = Column(JSONB, default=[])
    # [
    #   {
    #     "id": "ref_1",
    #     "name": "João Silva",
    #     "phone": "(11) 98888-8888",
    #     "relationship": "Irmão",
    #     "verified": false
    #   }
    # ]
    
    # Documentos Anexos (RG, CNH, Comprovante, etc)
    documents = Column(JSONB, default=[])
    # [{
    #   "id": "doc_1",
    #   "type": "rg_front",
    #   "name": "RG Frente.jpg",
    #   "url": "https://supabase.co/storage/...",
    #   "uploaded_at": "2024-11-24T10:00:00Z"
    # }]
    
    # Status e Aprovação
    status = Column(Enum(PersonStatus), default=PersonStatus.PENDING, nullable=False, index=True)
    approved_by_id = Column(UUID(as_uuid=True))
    approved_at = Column(DateTime(timezone=True))
    notes = Column(Text)  # Observações gerais
    
    # Financeiro (aplicável principalmente a CLIENTS)
    credit_limit = Column(Numeric(10, 2), default=0)
    defaulter = Column(Boolean, default=False, nullable=False, index=True)  # Inadimplente
    total_rentals = Column(Integer, default=0)  # Total de locações
    total_spent = Column(Numeric(10, 2), default=0)  # Total gasto
    
    # 🆕 Dados Específicos por Tipo (JSONB flexível)
    
    # Dados de Funcionário (se type inclui EMPLOYEE)
    employee_data = Column(JSONB)
    # {
    #   "position": "Gerente",
    #   "salary": 5000.00,
    #   "hire_date": "2024-01-15",
    #   "department": "Operações",
    #   "user_id": "uuid-do-usuario"  # Relacionamento com User para login
    # }
    
    # Dados de Freteiro/Motorista (se type inclui DRIVER)
    driver_data = Column(JSONB)
    # {
    #   "vehicle_type": "Fiorino",
    #   "license_plate": "ABC-1234",
    #   "drivers_license": "12345678901",
    #   "license_category": "B",
    #   "license_expiration": "2027-12-31",
    #   "available": true
    # }
    
    # Dados de Fornecedor (se type inclui SUPPLIER)
    supplier_data = Column(JSONB)
    # {
    #   "products": ["Betoneiras", "Andaimes"],
    #   "bank": "Banco do Brasil",
    #   "agency": "1234-5",
    #   "account": "67890-1",
    #   "payment_terms": "30 dias"
    # }
    
    # Dados de Parceiro (se type inclui PARTNER)
    partner_data = Column(JSONB)
    # {
    #   "partnership_type": "Indicação",
    #   "commission_rate": 10.0,
    #   "contract_url": "https://..."
    # }
    
    # Visibilidade
    active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Auditoria
    created_by_id = Column(UUID(as_uuid=True))
    updated_by_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Client since (para CLIENTs)
    customer_since = Column(DateTime(timezone=True))
    
    def __repr__(self):
        name = self.full_name or self.company_name or f"Person {self.id}"
        return f"<Person {name} ({', '.join(self.types or [])})>"
    
    @property
    def is_client(self) -> bool:
        """Verifica se a pessoa é cliente"""
        return PersonType.CLIENT in (self.types or [])
    
    @property
    def is_driver(self) -> bool:
        """Verifica se a pessoa é freteiro/motorista"""
        return PersonType.DRIVER in (self.types or [])
    
    @property
    def is_employee(self) -> bool:
        """Verifica se a pessoa é funcionário"""
        return PersonType.EMPLOYEE in (self.types or [])
    
    @property
    def is_supplier(self) -> bool:
        """Verifica se a pessoa é fornecedor"""
        return PersonType.SUPPLIER in (self.types or [])
    
    @property
    def display_name(self) -> str:
        """Nome para exibição"""
        if self.document_type == PersonDocumentType.CPF:
            return self.full_name or "Sem nome"
        else:
            return self.trade_name or self.company_name or "Sem nome"
    
    @property
    def formatted_document(self) -> str:
        """Documento formatado (CPF ou CNPJ)"""
        if self.document_type == PersonDocumentType.CPF and self.cpf:
            # Formata CPF: 000.000.000-00
            cpf = self.cpf
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif self.document_type == PersonDocumentType.CNPJ and self.cnpj:
            # Formata CNPJ: 00.000.000/0000-00
            cnpj = self.cnpj
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return "Sem documento"
    
    @property
    def full_address(self) -> str:
        """Endereço completo formatado"""
        if not self.address or not isinstance(self.address, dict):
            return "Endereço não cadastrado"
        
        parts = []
        if self.address.get('street'):
            parts.append(self.address['street'])
        if self.address.get('number'):
            parts.append(self.address['number'])
        if self.address.get('complement'):
            parts.append(self.address['complement'])
        if self.address.get('neighborhood'):
            parts.append(self.address['neighborhood'])
        if self.address.get('city') and self.address.get('state'):
            parts.append(f"{self.address['city']}/{self.address['state']}")
        if self.address.get('cep'):
            parts.append(f"CEP: {self.address['cep']}")
        
        return ", ".join(parts) if parts else "Endereço incompleto"
