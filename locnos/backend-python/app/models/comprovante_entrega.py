"""
Model SQLAlchemy para Comprovante de Entrega - Sistema Logística Droguista

Gerencia comprovantes digitais de entrega (e-POD - electronic Proof of Delivery).
Armazena assinaturas e fotos no Google Drive.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum, Numeric, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class StatusEntrega(str, enum.Enum):
    """Status da tentativa de entrega"""
    ENTREGUE = "entregue"              # Entregue com sucesso
    ENTREGA_PARCIAL = "entrega_parcial"  # Entregue parcialmente
    RECUSADO = "recusado"              # Cliente recusou receber
    AUSENTE = "ausente"                # Cliente ausente
    ENDERECO_INCORRETO = "endereco_incorreto"
    ADIADO = "adiado"                  # Cliente pediu para entregar depois
    DEVOLVIDO = "devolvido"            # Devolvido ao remetente


class TipoOcorrencia(str, enum.Enum):
    """Tipos de ocorrências na entrega"""
    NORMAL = "normal"                  # Entrega sem problemas
    ATRASO = "atraso"                  # Entrega atrasada
    CLIENTE_AUSENTE = "cliente_ausente"
    ENDERECO_NAO_LOCALIZADO = "endereco_nao_localizado"
    RECUSA_CLIENTE = "recusa_cliente"
    PRODUTO_AVARIADO = "produto_avariado"
    DIVERGENCIA_PEDIDO = "divergencia_pedido"
    AREA_RISCO = "area_risco"
    CONDICAO_CLIMATICA = "condicao_climatica"
    OUTROS = "outros"


class ComprovanteEntrega(Base):
    """
    Model de Comprovante de Entrega Digital (e-POD)
    
    Registra detalhes da entrega incluindo:
    - Assinatura digital do recebedor
    - Foto do comprovante
    - Geolocalização
    - Dados de quem recebeu
    - Ocorrências
    """
    
    __tablename__ = "comprovantes_entrega"
    
    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # =========================================================================
    # RELACIONAMENTOS
    # =========================================================================
    pedido_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pedidos.id"),
        nullable=False,
        unique=True,  # Um comprovante por pedido
        index=True
    )
    
    rota_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rotas.id"),
        index=True
    )
    
    motorista_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pessoas.id"),
        nullable=False,
        index=True
    )
    
    # =========================================================================
    # DATA E HORA DA ENTREGA
    # =========================================================================
    data_hora_entrega = Column(DateTime(timezone=True), nullable=False, index=True)
    data_hora_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # =========================================================================
    # STATUS DA ENTREGA
    # =========================================================================
    status_entrega = Column(
        Enum(StatusEntrega),
        default=StatusEntrega.ENTREGUE,
        nullable=False,
        index=True
    )
    
    entrega_bem_sucedida = Column(Boolean, default=True, index=True)
    
    # =========================================================================
    # DADOS DO RECEBEDOR
    # =========================================================================
    recebedor_nome = Column(String(200), nullable=False)
    recebedor_documento = Column(String(20))  # CPF ou RG
    recebedor_parentesco = Column(String(100))  # Ex: "Próprio", "Esposa", "Funcionário"
    recebedor_telefone = Column(String(20))
    
    # =========================================================================
    # ASSINATURA DIGITAL
    # =========================================================================
    assinatura_url = Column(String(500))  # URL da imagem no Google Drive
    assinatura_google_drive_id = Column(String(200))  # ID do arquivo no Google Drive
    assinatura_capturada = Column(Boolean, default=False)
    
    # =========================================================================
    # FOTO DO COMPROVANTE
    # =========================================================================
    foto_comprovante_url = Column(String(500))  # URL da foto no Google Drive
    foto_google_drive_id = Column(String(200))  # ID do arquivo no Google Drive
    foto_capturada = Column(Boolean, default=False)
    
    # Fotos adicionais (múltiplas fotos)
    fotos_adicionais = Column(JSONB, default=[])
    # [
    #   {
    #     "url": "https://drive.google.com/...",
    #     "google_drive_id": "1abc...",
    #     "descricao": "Foto do produto entregue",
    #     "data_hora": "2024-11-26T14:30:00Z"
    #   }
    # ]
    
    # =========================================================================
    # GEOLOCALIZAÇÃO
    # =========================================================================
    latitude = Column(Numeric(10, 8))  # Latitude com 8 casas decimais
    longitude = Column(Numeric(11, 8))  # Longitude com 8 casas decimais
    precisao_metros = Column(Numeric(10, 2))  # Precisão do GPS em metros
    geolocalizacao_capturada = Column(Boolean, default=False)
    
    # Endereço reverso (obtido da geolocalização)
    endereco_gps = Column(String(500))
    
    # =========================================================================
    # OBSERVAÇÕES E NOTAS
    # =========================================================================
    observacoes = Column(Text)  # Observações do motorista
    observacoes_cliente = Column(Text)  # Observações do cliente
    
    # =========================================================================
    # OCORRÊNCIAS
    # =========================================================================
    teve_ocorrencia = Column(Boolean, default=False, index=True)
    tipo_ocorrencia = Column(Enum(TipoOcorrencia), default=TipoOcorrencia.NORMAL)
    
    ocorrencias = Column(JSONB, default=[])
    # [
    #   {
    #     "tipo": "atraso",
    #     "descricao": "Trânsito na região",
    #     "data_hora": "2024-11-26T14:00:00Z",
    #     "resolvido": true
    #   }
    # ]
    
    # =========================================================================
    # TENTATIVAS DE ENTREGA
    # =========================================================================
    numero_tentativa = Column(Integer, default=1)  # Primeira tentativa = 1
    
    tentativas_anteriores = Column(JSONB, default=[])
    # [
    #   {
    #     "numero": 1,
    #     "data_hora": "2024-11-25T10:00:00Z",
    #     "motivo_falha": "Cliente ausente",
    #     "observacoes": "Vizinho informou retorno às 14h"
    #   }
    # ]
    
    # =========================================================================
    # VOLUMES ENTREGUES
    # =========================================================================
    volumes_entregues = Column(Integer)  # Quantos volumes foram entregues
    volumes_total = Column(Integer)  # Total de volumes do pedido
    entrega_completa = Column(Boolean, default=True)
    
    itens_divergentes = Column(JSONB, default=[])
    # [
    #   {
    #     "codigo": "PROD-001",
    #     "descricao": "Produto Exemplo",
    #     "quantidade_pedido": 10,
    #     "quantidade_entregue": 9,
    #     "motivo": "Produto avariado no transporte"
    #   }
    # ]
    
    # =========================================================================
    # GOOGLE DRIVE
    # =========================================================================
    google_drive_folder_id = Column(String(200))  # ID da pasta do pedido no Drive
    google_drive_folder_url = Column(String(500))  # URL da pasta
    
    # =========================================================================
    # AVALIAÇÃO DA ENTREGA
    # =========================================================================
    avaliacao_cliente = Column(Integer)  # De 1 a 5 estrelas
    comentario_cliente = Column(Text)
    
    # =========================================================================
    # DISPOSITIVO USADO PARA REGISTRO
    # =========================================================================
    dispositivo_info = Column(JSONB)
    # {
    #   "tipo": "smartphone",
    #   "modelo": "Samsung Galaxy A52",
    #   "sistema_operacional": "Android 12",
    #   "app_versao": "1.0.5",
    #   "online": true
    # }
    
    # =========================================================================
    # SINCRONIZAÇÃO
    # =========================================================================
    sincronizado = Column(Boolean, default=True)
    data_sincronizacao = Column(DateTime(timezone=True))
    
    # =========================================================================
    # METADATA E AUDITORIA
    # =========================================================================
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ComprovanteEntrega Pedido: {self.pedido_id} - Status: {self.status_entrega.value}>"
    
    @property
    def comprovante_completo(self) -> bool:
        """Verifica se o comprovante está completo"""
        if not self.entrega_bem_sucedida:
            # Para entregas não sucedidas, requer pelo menos observação do motivo
            return bool(self.observacoes)
        
        # Para entregas bem-sucedidas
        return (
            bool(self.recebedor_nome) and
            (self.assinatura_capturada or self.foto_capturada) and
            self.geolocalizacao_capturada
        )
    
    @property
    def tempo_desde_entrega(self) -> str:
        """Retorna tempo decorrido desde a entrega de forma legível"""
        from datetime import datetime, timezone
        
        if not self.data_hora_entrega:
            return "Não entregue"
        
        agora = datetime.now(timezone.utc)
        delta = agora - self.data_hora_entrega
        
        if delta.days > 0:
            return f"{delta.days} dia(s) atrás"
        
        horas = delta.seconds // 3600
        if horas > 0:
            return f"{horas} hora(s) atrás"
        
        minutos = (delta.seconds % 3600) // 60
        return f"{minutos} minuto(s) atrás"
    
    @property
    def coordenadas_formatadas(self) -> str:
        """Retorna coordenadas formatadas"""
        if not self.latitude or not self.longitude:
            return "Sem coordenadas"
        
        return f"{float(self.latitude):.6f}, {float(self.longitude):.6f}"
    
    @property
    def link_google_maps(self) -> str:
        """Gera link do Google Maps para as coordenadas"""
        if not self.latitude or not self.longitude:
            return ""
        
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
    
    def adicionar_ocorrencia(self, tipo: str, descricao: str):
        """
        Adiciona uma ocorrência ao comprovante
        
        Args:
            tipo: Tipo da ocorrência
            descricao: Descrição detalhada
        """
        from datetime import datetime, timezone
        
        if not isinstance(self.ocorrencias, list):
            self.ocorrencias = []
        
        ocorrencia = {
            "tipo": tipo,
            "descricao": descricao,
            "data_hora": datetime.now(timezone.utc).isoformat(),
            "resolvido": False
        }
        
        self.ocorrencias.append(ocorrencia)
        self.teve_ocorrencia = True
    
    def adicionar_foto_adicional(self, url: str, google_drive_id: str, descricao: str = ""):
        """
        Adiciona uma foto adicional ao comprovante
        
        Args:
            url: URL da foto no Google Drive
            google_drive_id: ID do arquivo no Google Drive
            descricao: Descrição da foto
        """
        from datetime import datetime, timezone
        
        if not isinstance(self.fotos_adicionais, list):
            self.fotos_adicionais = []
        
        foto = {
            "url": url,
            "google_drive_id": google_drive_id,
            "descricao": descricao,
            "data_hora": datetime.now(timezone.utc).isoformat()
        }
        
        self.fotos_adicionais.append(foto)
