"""
Model SQLAlchemy para Pedidos - Sistema Logística Droguista

Este modelo representa o pedido no fluxo de expedição logística,
desde o faturamento no ERP até a entrega final ao cliente.
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class StatusPedido(str, enum.Enum):
    """Status do pedido no fluxo de expedição"""
    PENDENTE_EXPEDICAO = "pendente_expedicao"      # Faturado, aguardando separação
    EM_SEPARACAO = "em_separacao"                  # Sendo separado no armazém
    SEPARADO = "separado"                          # Separação concluída
    EM_CONFERENCIA = "em_conferencia"              # Sendo conferido
    CONFERIDO = "conferido"                        # Conferência concluída
    AGUARDANDO_CARGA = "aguardando_carga"          # Pronto, aguardando formar carga/rota
    EXPEDIDO = "expedido"                          # Saiu do armazém
    EM_ROTA = "em_rota"                            # Em trânsito para entrega
    ENTREGUE = "entregue"                          # Entregue ao cliente
    CANCELADO = "cancelado"                        # Pedido cancelado
    ENTREGA_FALHOU = "entrega_falhou"              # Tentativa de entrega não sucedida


class TipoFrete(str, enum.Enum):
    """Tipo de frete do pedido"""
    CIF = "cif"  # Cliente paga frete (Custo, Seguro e Frete)
    FOB = "fob"  # Fornecedor paga frete (Free On Board)


class Pedido(Base):
    """
    Model de Pedido para Expedição Logística
    
    Representa um pedido faturado que precisa ser expedido e entregue.
    Integra com ERP (SAP B1) e WMS (Expert) para sincronização de dados.
    """
    
    __tablename__ = "pedidos"
    
    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_pedido = Column(String(50), unique=True, nullable=False, index=True)
    numero_nf = Column(String(50), index=True)  # Número da Nota Fiscal
    
    # =========================================================================
    # DATAS
    # =========================================================================
    data_pedido = Column(DateTime(timezone=True), nullable=False, index=True)
    data_faturamento = Column(DateTime(timezone=True), index=True)
    data_prevista_entrega = Column(DateTime(timezone=True))
    
    # =========================================================================
    # CLIENTE E VENDEDOR
    # =========================================================================
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"), nullable=False, index=True)
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"), index=True)
    
    # =========================================================================
    # LOCALIZAÇÃO E ENTREGA
    # =========================================================================
    regiao_entrega = Column(String(100), index=True)  # Região/Cidade de destino
    endereco_entrega = Column(JSONB, nullable=False)
    # {
    #   "cep": "01310-100",
    #   "logradouro": "Av Paulista",
    #   "numero": "1578",
    #   "complemento": "Sala 10",
    #   "bairro": "Bela Vista",
    #   "cidade": "São Paulo",
    #   "estado": "SP",
    #   "referencia": "Próximo ao Metrô Trianon"
    # }
    
    # =========================================================================
    # STATUS E WORKFLOW
    # =========================================================================
    status = Column(
        Enum(StatusPedido),
        default=StatusPedido.PENDENTE_EXPEDICAO,
        nullable=False,
        index=True
    )
    
    # =========================================================================
    # TRANSPORTADORA E FROTA
    # =========================================================================
    transportadora_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transportadoras.id"),
        nullable=True,
        index=True
    )
    veiculo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("veiculos.id"),
        nullable=True,
        index=True
    )
    rota_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rotas.id"),
        nullable=True,
        index=True
    )
    
    # =========================================================================
    # FRETE
    # =========================================================================
    tipo_frete = Column(Enum(TipoFrete), default=TipoFrete.CIF, nullable=False)
    valor_frete = Column(Numeric(10, 2), default=0)
    
    # =========================================================================
    # DIMENSÕES E PESO
    # =========================================================================
    peso_total_kg = Column(Numeric(10, 3), default=0)  # Peso total em kg
    volumes = Column(Integer, default=1)  # Quantidade de caixas/volumes
    cubagem_m3 = Column(Numeric(10, 3))  # Cubagem em m³ (opcional)
    
    # =========================================================================
    # VALORES
    # =========================================================================
    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_produtos = Column(Numeric(10, 2))
    valor_descontos = Column(Numeric(10, 2), default=0)
    
    # =========================================================================
    # ITENS DO PEDIDO
    # =========================================================================
    itens = Column(JSONB, default=[])
    # [
    #   {
    #     "codigo": "PROD-001",
    #     "descricao": "Produto Exemplo",
    #     "quantidade": 10,
    #     "unidade": "UN",
    #     "valor_unitario": 25.50,
    #     "valor_total": 255.00,
    #     "codigo_barras": "7891234567890"
    #   }
    # ]
    
    # =========================================================================
    # RASTREABILIDADE - SEPARAÇÃO
    # =========================================================================
    separador_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"))
    data_separacao = Column(DateTime(timezone=True))
    observacoes_separacao = Column(Text)
    
    # =========================================================================
    # RASTREABILIDADE - CONFERÊNCIA
    # =========================================================================
    conferente_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"))
    data_conferencia = Column(DateTime(timezone=True))
    observacoes_conferencia = Column(Text)
    divergencias_conferencia = Column(JSONB, default=[])
    # [
    #   {
    #     "tipo": "falta",
    #     "codigo_produto": "PROD-001",
    #     "quantidade_esperada": 10,
    #     "quantidade_encontrada": 9,
    #     "descricao": "Falta 1 unidade"
    #   }
    # ]
    
    # =========================================================================
    # RASTREABILIDADE - EXPEDIÇÃO
    # =========================================================================
    expedidor_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"))
    data_expedicao = Column(DateTime(timezone=True), index=True)
    hora_saida_veiculo = Column(DateTime(timezone=True))
    
    # =========================================================================
    # RASTREABILIDADE - ENTREGA
    # =========================================================================
    motorista_id = Column(UUID(as_uuid=True), ForeignKey("pessoas.id"))
    data_entrega = Column(DateTime(timezone=True), index=True)
    
    # =========================================================================
    # RASTREAMENTO
    # =========================================================================
    codigo_rastreio = Column(String(100), index=True)  # Código de rastreio (transportadora)
    url_rastreamento = Column(String(500))  # URL para rastreamento externo
    
    # =========================================================================
    # OBSERVAÇÕES E INSTRUÇÕES
    # =========================================================================
    observacoes = Column(Text)  # Observações gerais
    observacoes_entrega = Column(Text)  # Instruções específicas de entrega
    observacoes_internas = Column(Text)  # Notas internas (não vão para o motorista)
    
    # =========================================================================
    # PRIORIDADE
    # =========================================================================
    urgente = Column(Boolean, default=False, index=True)  # Entrega urgente
    prioridade = Column(Integer, default=0)  # 0=Normal, 1=Alta, 2=Urgente
    
    # =========================================================================
    # INTEGRAÇÃO ERP/WMS
    # =========================================================================
    erp_pedido_id = Column(String(50))  # ID do pedido no ERP (SAP B1)
    erp_sincronizado = Column(Boolean, default=False)
    erp_ultima_sincronizacao = Column(DateTime(timezone=True))
    
    wms_pedido_id = Column(String(50))  # ID do pedido no WMS (Expert)
    wms_sincronizado = Column(Boolean, default=False)
    wms_ultima_sincronizacao = Column(DateTime(timezone=True))
    
    # =========================================================================
    # METADATA E AUDITORIA
    # =========================================================================
    ativo = Column(Boolean, default=True, nullable=False, index=True)
    
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    atualizado_por_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Pedido {self.numero_pedido} - Status: {self.status.value}>"
    
    @property
    def pode_separar(self) -> bool:
        """Verifica se o pedido pode ser separado"""
        return self.status == StatusPedido.PENDENTE_EXPEDICAO
    
    @property
    def pode_conferir(self) -> bool:
        """Verifica se o pedido pode ser conferido"""
        return self.status == StatusPedido.SEPARADO
    
    @property
    def pode_expedir(self) -> bool:
        """Verifica se o pedido pode ser expedido"""
        return self.status == StatusPedido.CONFERIDO
    
    @property
    def esta_em_atraso(self) -> bool:
        """Verifica se o pedido está em atraso"""
        if not self.data_prevista_entrega:
            return False
        
        from datetime import datetime, timezone
        agora = datetime.now(timezone.utc)
        
        return (
            self.status not in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO] and
            agora > self.data_prevista_entrega
        )
    
    @property
    def dias_desde_faturamento(self) -> int:
        """Calcula quantos dias desde o faturamento"""
        if not self.data_faturamento:
            return 0
        
        from datetime import datetime, timezone
        agora = datetime.now(timezone.utc)
        delta = agora - self.data_faturamento
        
        return delta.days
    
    @property
    def endereco_entrega_formatado(self) -> str:
        """Retorna endereço de entrega formatado"""
        if not self.endereco_entrega or not isinstance(self.endereco_entrega, dict):
            return "Endereço não cadastrado"
        
        end = self.endereco_entrega
        partes = []
        
        if end.get('logradouro'):
            partes.append(end['logradouro'])
        if end.get('numero'):
            partes.append(end['numero'])
        if end.get('complemento'):
            partes.append(end['complemento'])
        if end.get('bairro'):
            partes.append(end['bairro'])
        if end.get('cidade') and end.get('estado'):
            partes.append(f"{end['cidade']}/{end['estado']}")
        if end.get('cep'):
            partes.append(f"CEP: {end['cep']}")
        
        return ", ".join(partes) if partes else "Endereço incompleto"
