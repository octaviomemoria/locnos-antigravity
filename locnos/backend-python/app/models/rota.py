"""
Model SQLAlchemy para Rotas - Sistema Logística Droguista

Gerencia rotas de entrega e formação de cargas.
"""

from sqlalchemy import Column, String, Boolean, Integer, Date, DateTime, Enum, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class TipoRota(str, enum.Enum):
    """Tipo de execução da rota"""
    FROTA_PROPRIA = "frota_propria"      # Entrega com frota própria
    TRANSPORTADORA = "transportadora"     # Entrega terceirizada


class StatusRota(str, enum.Enum):
    """Status da rota no fluxo logístico"""
    PLANEJADA = "planejada"              # Rota criada, pedidos selecionados
    EM_CARREGAMENTO = "em_carregamento"  # Veículo sendo carregado
    CARREGADA = "carregada"              # Carregamento concluído
    EM_ROTA = "em_rota"                  # Veículo saiu para entregas
    FINALIZADA = "finalizada"            # Todas entregas concluídas
    CANCELADA = "cancelada"              # Rota cancelada


class Rota(Base):
    """
    Model de Rota
    
    Representa uma rota de entrega com conjunto de pedidos.
    Pode ser executada por frota própria ou transportadora.
    """
    
    __tablename__ = "rotas"
    
    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    # Formato sugerido: RTA-2024-001, RTA-2024-002, etc.
    
    descricao = Column(String(200))  # Descrição da rota (ex: "Zona Sul - SP")
    
    # =========================================================================
    # TIPO E DATAS
    # =========================================================================
    tipo = Column(Enum(TipoRota), nullable=False, index=True)
    
    data_planejada = Column(Date, nullable=False, index=True)  # Data planejada para entregas
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    
    # =========================================================================
    # VEÍCULO OU TRANSPORTADORA
    # =========================================================================
    veiculo_id = Column(
        UUID(as_uuid=True),
        ForeignKey("veiculos.id"),
        nullable=True,
        index=True
    )
    
    transportadora_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transportadoras.id"),
        nullable=True,
        index=True
    )
    
    # =========================================================================
    # MOTORISTA
    # =========================================================================
    motorista_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pessoas.id"),
        nullable=True,
        index=True
    )
    
    # =========================================================================
    # REGIÃO E CARACTERÍSTICAS
    # =========================================================================
    regiao_principal = Column(String(100), index=True)  # Região predominante da rota
    cidade_principal = Column(String(100))
    estado = Column(String(2))
    
    # =========================================================================
    # STATUS
    # =========================================================================
    status = Column(
        Enum(StatusRota),
        default=StatusRota.PLANEJADA,
        nullable=False,
        index=True
    )
    
    # =========================================================================
    # PEDIDOS DA ROTA
    # =========================================================================
    pedidos_ids = Column(JSONB, default=[])
    # Lista de UUIDs dos pedidos: ["uuid-1", "uuid-2", "uuid-3"]
    
    quantidade_pedidos = Column(Integer, default=0)
    quantidade_entregas_concluidas = Column(Integer, default=0)
    quantidade_entregas_falhadas = Column(Integer, default=0)
    
    # =========================================================================
    # SEQUÊNCIA DE ENTREGAS (ROTEIRIZAÇÃO)
    # =========================================================================
    sequencia_entregas = Column(JSONB, default=[])
    # [
    #   {
    #     "ordem": 1,
    #     "pedido_id": "uuid-abc",
    #     "cliente": "João Silva",
    #     "endereco": "Rua A, 123",
    #     "latitude": -23.550520,
    #     "longitude": -46.633308,
    #     "tempo_estimado_minutos": 15,
    #     "status": "pendente" | "entregue" | "falhou"
    #   }
    # ]
    
    otimizada = Column(Boolean, default=False)  # Se a sequência foi otimizada
    algoritmo_otimizacao = Column(String(50))  # Ex: "guloso", "nearest_neighbor"
    
    # =========================================================================
    # DISTÂNCIA E TEMPO
    # =========================================================================
    distancia_total_km = Column(Numeric(10, 2))  # Distância total estimada
    tempo_estimado_minutos = Column(Integer)  # Tempo total estimado
    
    # =========================================================================
    # HORÁRIOS
    # =========================================================================
    hora_inicio_carregamento = Column(DateTime(timezone=True))
    hora_fim_carregamento = Column(DateTime(timezone=True))
    hora_saida = Column(DateTime(timezone=True), index=True)
    hora_retorno_estimado = Column(DateTime(timezone=True))
    hora_retorno_real = Column(DateTime(timezone=True))
    
    # =========================================================================
    # CAPACIDADE E CARGA
    # =========================================================================
    peso_total_kg = Column(Numeric(10, 2), default=0)
    volume_total_m3 = Column(Numeric(10, 3))
    total_volumes = Column(Integer, default=0)  # Soma de volumes de todos os pedidos
    
    # Verificação de capacidade
    capacidade_peso_utilizada_percent = Column(Numeric(5, 2))  # % de capacidade usada
    capacidade_volume_utilizada_percent = Column(Numeric(5, 2))
    
    # =========================================================================
    # CUSTOS
    # =========================================================================
    custo_total = Column(Numeric(10, 2), default=0)
    
    custos_detalhados = Column(JSONB, default={})
    # {
    #   "combustivel": 150.00,
    #   "pedagios": 25.00,
    #   "motorista": 200.00,
    #   "manutencao": 50.00,
    #   "outros": 10.00
    # }
    
    # =========================================================================
    # DOCUMENTOS
    # =========================================================================
    romaneio_url = Column(String(500))  # URL do PDF do romaneio
    manifesto_url = Column(String(500))  # URL do manifesto de carga
    
    # =========================================================================
    # OBSERVAÇÕES E INSTRUÇÕES
    # =========================================================================
    observacoes = Column(Text)
    instrucoes_motorista = Column(Text)
    restricoes = Column(Text)
    
    # =========================================================================
    # MONITORAMENTO
    # =========================================================================
    localizacao_atual = Column(JSONB)
    # {
    #   "latitude": -23.550520,
    #   "longitude": -46.633308,
    #   "data_hora": "2024-11-26T14:30:00Z",
    #   "precisao_metros": 10
    # }
    
    historico_localizacoes = Column(JSONB, default=[])
    # Array de localizações durante a rota
    
    # =========================================================================
    # OCORRÊNCIAS
    # =========================================================================
    ocorrencias = Column(JSONB, default=[])
    # [
    #   {
    #     "data_hora": "2024-11-26T15:00:00Z",
    #     "tipo": "atraso" | "acidente" | "pneu_furado" | "outros",
    #     "descricao": "Trânsito intenso na Marginal",
    #     "impacto_minutos": 30
    #   }
    # ]
    
    # =========================================================================
    # ESTATÍSTICAS
    # =========================================================================
    taxa_sucesso_entregas = Column(Numeric(5, 2))  # % de entregas bem-sucedidas
    tempo_medio_entrega_minutos = Column(Integer)
    km_final = Column(Numeric(10, 2))  # Quilometragem final percorrida
    
    # =========================================================================
    # APROVAÇÃO E CONTROLE
    # =========================================================================
    aprovada = Column(Boolean, default=False)
    aprovada_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    data_aprovacao = Column(DateTime(timezone=True))
    
    # =========================================================================
    # METADATA E AUDITORIA
    # =========================================================================
    ativa = Column(Boolean, default=True, nullable=False, index=True)
    
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    atualizado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Rota {self.codigo} - {self.status.value}>"
    
    @property
    def em_andamento(self) -> bool:
        """Verifica se a rota está em andamento"""
        return self.status in [StatusRota.EM_CARREGAMENTO, StatusRota.CARREGADA, StatusRota.EM_ROTA]
    
    @property
    def pode_ser_editada(self) -> bool:
        """Verifica se a rota ainda pode ser editada"""
        return self.status in [StatusRota.PLANEJADA, StatusRota.EM_CARREGAMENTO]
    
    @property
    def todas_entregas_concluidas(self) -> bool:
        """Verifica se todas as entregas foram concluídas"""
        if self.quantidade_pedidos == 0:
            return False
        
        total_concluidas = self.quantidade_entregas_concluidas + self.quantidade_entregas_falhadas
        return total_concluidas >= self.quantidade_pedidos
    
    @property
    def progresso_percentual(self) -> float:
        """Calcula percentual de progresso das entregas"""
        if self.quantidade_pedidos == 0:
            return 0.0
        
        total_concluidas = self.quantidade_entregas_concluidas + self.quantidade_entregas_falhadas
        return (total_concluidas / self.quantidade_pedidos) * 100
    
    @property
    def duracao_real_minutos(self) -> int:
        """Calcula duração real da rota em minutos"""
        if not self.hora_saida:
            return 0
        
        hora_fim = self.hora_retorno_real or datetime.now(timezone.utc)
        delta = hora_fim - self.hora_saida
        
        return int(delta.total_seconds() / 60)
    
    @property
    def esta_atrasada(self) -> bool:
        """Verifica se a rota está atrasada em relação ao estimado"""
        if not self.hora_retorno_estimado:
            return False
        
        from datetime import datetime, timezone
        agora = datetime.now(timezone.utc)
        
        return (
            self.status == StatusRota.EM_ROTA and
            agora > self.hora_retorno_estimado
        )
    
    def adicionar_pedido(self, pedido_id: str, ordem: int = None):
        """
        Adiciona um pedido à rota
        
        Args:
            pedido_id: UUID do pedido
            ordem: Posição na sequência (opcional)
        """
        if not isinstance(self.pedidos_ids, list):
            self.pedidos_ids = []
        
        if pedido_id not in self.pedidos_ids:
            self.pedidos_ids.append(pedido_id)
            self.quantidade_pedidos = len(self.pedidos_ids)
    
    def remover_pedido(self, pedido_id: str):
        """
        Remove um pedido da rota
        
        Args:
            pedido_id: UUID do pedido
        """
        if isinstance(self.pedidos_ids, list) and pedido_id in self.pedidos_ids:
            self.pedidos_ids.remove(pedido_id)
            self.quantidade_pedidos = len(self.pedidos_ids)
    
    def calcular_eficiencia(self) -> dict:
        """
        Calcula métricas de eficiência da rota
        
        Returns:
            Dicionário com métricas de eficiência
        """
        eficiencia = {
            "taxa_sucesso": float(self.taxa_sucesso_entregas or 0),
            "entregas_por_hora": 0,
            "km_por_entrega": 0,
            "custo_por_entrega": 0,
            "pontualidade": 100.0  # % no prazo
        }
        
        # Entregas por hora
        if self.duracao_real_minutos > 0 and self.quantidade_entregas_concluidas > 0:
            horas = self.duracao_real_minutos / 60
            eficiencia["entregas_por_hora"] = self.quantidade_entregas_concluidas / horas
        
        # Km por entrega
        if self.km_final and self.quantidade_entregas_concluidas > 0:
            eficiencia["km_por_entrega"] = float(self.km_final) / self.quantidade_entregas_concluidas
        
        # Custo por entrega
        if self.custo_total and self.quantidade_entregas_concluidas > 0:
            eficiencia["custo_por_entrega"] = float(self.custo_total) / self.quantidade_entregas_concluidas
        
        # Pontualidade (placeholder - requer dados de entregas individuais)
        if not self.esta_atrasada:
            eficiencia["pontualidade"] = 100.0
        else:
            eficiencia["pontualidade"] = 75.0  # Exemplo
        
        return eficiencia
