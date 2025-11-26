"""
Model SQLAlchemy para Veículos - Sistema Logística Droguista

Gerencia a frota própria de veículos para entregas.
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class TipoVeiculo(str, enum.Enum):
    """Tipos de veículos da frota"""
    MOTO = "moto"
    FIORINO = "fiorino"
    VAN = "van"
    CAMINHAO_3_4 = "caminhao_3_4"  # Caminhão 3/4
    CAMINHAO_TOCO = "caminhao_toco"
    CAMINHAO_TRUCK = "caminhao_truck"
    CARRETA = "carreta"
    UTILITARIO = "utilitario"


class StatusVeiculo(str, enum.Enum):
    """Status operacional do veículo"""
    DISPONIVEL = "disponivel"
    EM_ROTA = "em_rota"
    MANUTENCAO = "manutencao"
    INATIVO = "inativo"
    VENDIDO = "vendido"


class Veiculo(Base):
    """
    Model de Veículo
    
    Representa um veículo da frota própria para entregas.
    Inclui controle de capacidade, manutenção e custos operacionais.
    """
    
    __tablename__ = "veiculos"
    
    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    placa = Column(String(10), unique=True, nullable=False, index=True)
    tipo = Column(Enum(TipoVeiculo), nullable=False, index=True)
    
    # =========================================================================
    # DADOS DO VEÍCULO
    # =========================================================================
    marca = Column(String(100))
    modelo = Column(String(100))
    ano_fabricacao = Column(Integer)
    ano_modelo = Column(Integer)
    cor = Column(String(50))
    renavam = Column(String(20))
    chassi = Column(String(50))
    
    # =========================================================================
    # CAPACIDADES
    # =========================================================================
    capacidade_peso_kg = Column(Numeric(10, 2), nullable=False)  # Capacidade máxima em kg
    capacidade_volume_m3 = Column(Numeric(10, 3))  # Capacidade em metros cúbicos
    
    # Dimensões da área de carga
    comprimento_carga_m = Column(Numeric(5, 2))
    largura_carga_m = Column(Numeric(5, 2))
    altura_carga_m = Column(Numeric(5, 2))
    
    # =========================================================================
    # MOTORISTA PADRÃO
    # =========================================================================
    motorista_padrao_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pessoas.id"),
        nullable=True
    )
    # Relacionamento com Pessoa (tipo DRIVER)
    
    # =========================================================================
    # STATUS OPERACIONAL
    # =========================================================================
    status = Column(
        Enum(StatusVeiculo),
        default=StatusVeiculo.DISPONIVEL,
        nullable=False,
        index=True
    )
    disponivel = Column(Boolean, default=True, index=True)
    em_manutencao = Column(Boolean, default=False, index=True)
    
    # =========================================================================
    # QUILOMETRAGEM E MANUTENÇÃO
    # =========================================================================
    km_atual = Column(Integer, default=0)
    km_ultima_manutencao = Column(Integer)
    km_proxima_manutencao = Column(Integer)
    intervalo_manutencao_km = Column(Integer, default=10000)
    
    data_ultima_manutencao = Column(DateTime(timezone=True))
    data_proxima_manutencao = Column(DateTime(timezone=True))
    
    historico_manutencoes = Column(JSONB, default=[])
    # [
    #   {
    #     "data": "2024-11-20",
    #     "km": 45000,
    #     "tipo": "Preventiva",
    #     "descricao": "Troca de óleo e filtros",
    #     "valor": 350.00,
    #     "oficina": "Auto Mecânica Silva"
    #   }
    # ]
    
    # =========================================================================
    # DOCUMENTAÇÃO
    # =========================================================================
    data_vencimento_licenciamento = Column(DateTime(timezone=True))
    data_vencimento_seguro = Column(DateTime(timezone=True))
    
    seguradora = Column(String(200))
    numero_apolice = Column(String(50))
    valor_seguro = Column(Numeric(10, 2))
    
    # =========================================================================
    # CONSUMO E CUSTOS
    # =========================================================================
    consumo_medio_km_l = Column(Numeric(5, 2))  # Km por litro
    custo_km = Column(Numeric(10, 4))  # Custo por quilômetro rodado
    
    custos_mensais = Column(JSONB, default={})
    # {
    #   "combustivel": 1500.00,
    #   "manutencao": 300.00,
    #   "seguro": 250.00,
    #   "ipva": 150.00,
    #   "pedagios": 100.00,
    #   "outros": 50.00
    # }
    
    # =========================================================================
    # RASTREAMENTO E TECNOLOGIA
    # =========================================================================
    possui_rastreador = Column(Boolean, default=False)
    rastreador_id = Column(String(100))  # ID do rastreador
    rastreador_empresa = Column(String(100))  # Empresa de rastreamento
    
    possui_bau_refrigerado = Column(Boolean, default=False)
    possui_carroceria = Column(Boolean, default=False)
    tipo_carroceria = Column(String(100))  # Ex: "Baú", "Aberta", "Refrigerada"
    
    # =========================================================================
    # RESTRIÇÕES E CARACTERÍSTICAS
    # =========================================================================
    restricoes_circulacao = Column(Text)
    # Ex: "Não pode circular no centro expandido de SP das 7h às 10h e 17h às 20h"
    
    observacoes = Column(Text)
    
    # =========================================================================
    # ESTATÍSTICAS DE USO
    # =========================================================================
    total_entregas_realizadas = Column(Integer, default=0)
    total_km_rodados = Column(Integer, default=0)
    total_rotas_realizadas = Column(Integer, default=0)
    
    # =========================================================================
    # AQUISIÇÃO
    # =========================================================================
    data_aquisicao = Column(DateTime(timezone=True))
    valor_aquisicao = Column(Numeric(10, 2))
    valor_atual = Column(Numeric(10, 2))  # Valor de mercado atual
    fornecedor_aquisicao = Column(String(200))
    
    # =========================================================================
    # IMAGENS E DOCUMENTOS
    # =========================================================================
    imagens = Column(JSONB, default=[])
    # [
    #   {
    #     "tipo": "principal",
    #     "url": "https://...",
    #     "descricao": "Foto frontal do veículo"
    #   }
    # ]
    
    documentos = Column(JSONB, default=[])
    # [
    #   {
    #     "tipo": "crlv",
    #     "nome": "CRLV 2024.pdf",
    #     "url": "https://...",
    #     "data_upload": "2024-11-26"
    #   }
    # ]
    
    # =========================================================================
    # METADATA E AUDITORIA
    # =========================================================================
    ativo = Column(Boolean, default=True, nullable=False, index=True)
    
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    atualizado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Veiculo {self.placa} - {self.tipo.value}>"
    
    @property
    def disponivel_para_rota(self) -> bool:
        """Verifica se o veículo está disponível para criar uma rota"""
        return (
            self.ativo and
            self.disponivel and
            not self.em_manutencao and
            self.status == StatusVeiculo.DISPONIVEL
        )
    
    @property
    def precisa_manutencao(self) -> bool:
        """Verifica se o veículo está próximo ou passou do prazo de manutenção"""
        if self.km_proxima_manutencao and self.km_atual:
            # Alerta se faltam menos de 500 km para manutenção
            return (self.km_proxima_manutencao - self.km_atual) <= 500
        
        if self.data_proxima_manutencao:
            from datetime import datetime, timezone, timedelta
            agora = datetime.now(timezone.utc)
            # Alerta se faltam menos de 7 dias
            return (self.data_proxima_manutencao - agora) <= timedelta(days=7)
        
        return False
    
    @property
    def documentacao_em_dia(self) -> bool:
        """Verifica se a documentação do veículo está em dia"""
        from datetime import datetime, timezone
        agora = datetime.now(timezone.utc)
        
        if self.data_vencimento_licenciamento and self.data_vencimento_licenciamento < agora:
            return False
        
        if self.data_vencimento_seguro and self.data_vencimento_seguro < agora:
            return False
        
        return True
    
    @property
    def placa_formatada(self) -> str:
        """Retorna placa formatada (padrão Mercosul ou antigo)"""
        if not self.placa:
            return ""
        
        placa = self.placa.upper().replace("-", "").replace(" ", "")
        
        # Formato Mercosul: ABC1D23
        if len(placa) == 7:
            return f"{placa[:3]}{placa[3]}{placa[4]}{placa[5:]}"
        
        # Formato antigo: ABC-1234
        return f"{placa[:3]}-{placa[3:]}"
    
    @property
    def capacidade_utilizada_percentual(self) -> float:
        """
        Calcula percentual de capacidade utilizada (placeholder)
        Seria calculado com base nas cargas atuais
        """
        # TODO: Implementar cálculo real baseado em cargas em rota
        return 0.0
    
    def calcular_custo_rota(self, distancia_km: float) -> float:
        """
        Calcula custo estimado para uma rota
        
        Args:
            distancia_km: Distância da rota em quilômetros
        
        Returns:
            Custo estimado total
        """
        if not self.custo_km:
            return 0.0
        
        return float(self.custo_km) * distancia_km
    
    def pode_carregar(self, peso_kg: float, volume_m3: float = None) -> bool:
        """
        Verifica se o veículo pode carregar determinado peso/volume
        
        Args:
            peso_kg: Peso da carga em kg
            volume_m3: Volume da carga em m³ (opcional)
        
        Returns:
            True se o veículo comporta a carga
        """
        if peso_kg > float(self.capacidade_peso_kg):
            return False
        
        if volume_m3 and self.capacidade_volume_m3:
            if volume_m3 > float(self.capacidade_volume_m3):
                return False
        
        return True
