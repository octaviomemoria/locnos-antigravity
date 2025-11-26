"""
Model SQLAlchemy para Transportadoras - Sistema Logística Droguista

Gerencia cadastro de transportadoras terceirizadas para entregas.
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Transportadora(Base):
    """
    Model de Transportadora
    
    Cadastro de transportadoras terceirizadas para realizar entregas.
    Inclui regiões atendidas, custos e condições comerciais.
    """
    
    __tablename__ = "transportadoras"
    
    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(200), nullable=False, index=True)
    razao_social = Column(String(200))
    nome_fantasia = Column(String(200))
    
    # =========================================================================
    # DOCUMENTAÇÃO
    # =========================================================================
    cnpj = Column(String(14), unique=True, index=True)
    inscricao_estadual = Column(String(20))
    inscricao_municipal = Column(String(20))
    
    # =========================================================================
    # CONTATO
    # =========================================================================
    contato_nome = Column(String(200))  # Nome da pessoa de contato
    email = Column(String(255))
    telefone = Column(String(20))
    whatsapp = Column(String(20))
    
    # =========================================================================
    # ENDEREÇO
    # =========================================================================
    endereco = Column(JSONB)
    # {
    #   "cep": "01310-100",
    #   "logradouro": "Rua Exemplo",
    #   "numero": "123",
    #   "complemento": "Galpão 5",
    #   "bairro": "Centro",
    #   "cidade": "São Paulo",
    #   "estado": "SP"
    # }
    
    # =========================================================================
    # REGIÕES ATENDIDAS
    # =========================================================================
    regioes_atendidas = Column(JSONB, default=[])
    # [
    #   "São Paulo - SP",
    #   "Campinas - SP",
    #   "Santos - SP",
    #   "Região Metropolitana SP"
    # ]
    
    cidades_atendidas = Column(JSONB, default=[])
    # [
    #   {"cidade": "São Paulo", "estado": "SP", "prazo_dias": 1},
    #   {"cidade": "Campinas", "estado": "SP", "prazo_dias": 2}
    # ]
    
    # =========================================================================
    # CUSTOS E PRECIFICAÇÃO
    # =========================================================================
    custo_por_kg = Column(Numeric(10, 2))  # Custo por quilograma
    custo_por_entrega = Column(Numeric(10, 2))  # Custo fixo por entrega
    valor_minimo_frete = Column(Numeric(10, 2))  # Valor mínimo de frete
    
    # Tabela de frete customizada (opcional, mais flexível)
    tabela_frete = Column(JSONB, default=[])
    # [
    #   {
    #     "faixa_peso_inicial": 0,
    #     "faixa_peso_final": 10,
    #     "valor_kg": 5.00,
    #     "valor_fixo": 25.00
    #   },
    #   {
    #     "faixa_peso_inicial": 10,
    #     "faixa_peso_final": 50,
    #     "valor_kg": 4.00,
    #     "valor_fixo": 50.00
    #   }
    # ]
    
    # =========================================================================
    # PRAZOS
    # =========================================================================
    prazo_medio_entrega_dias = Column(Integer, default=3)  # Prazo médio
    prazo_coleta_horas = Column(Integer, default=24)  # Tempo para coletar após solicitação
    
    # =========================================================================
    # CONDIÇÕES COMERCIAIS
    # =========================================================================
    forma_pagamento = Column(String(100))  # Ex: "Quinzenal", "Mensal", "À vista"
    dia_vencimento = Column(Integer)  # Dia do mês para pagamento
    observacoes_comerciais = Column(Text)
    
    # =========================================================================
    # DADOS BANCÁRIOS
    # =========================================================================
    dados_bancarios = Column(JSONB)
    # {
    #   "banco": "001 - Banco do Brasil",
    #   "agencia": "1234-5",
    #   "conta": "67890-1",
    #   "tipo_conta": "Corrente",
    #   "pix": "12.345.678/0001-90"
    # }
    
    # =========================================================================
    # CAPACIDADES E RESTRIÇÕES
    # =========================================================================
    peso_maximo_kg = Column(Numeric(10, 2))  # Peso máximo que aceita
    volume_maximo_m3 = Column(Numeric(10, 3))  # Volume máximo
    aceita_carga_fracionada = Column(Boolean, default=True)
    aceita_carga_fechada = Column(Boolean, default=True)
    aceita_coleta = Column(Boolean, default=True)  # Faz coleta no remetente
    
    # =========================================================================
    # RASTREAMENTO
    # =========================================================================
    possui_rastreamento = Column(Boolean, default=False)
    url_rastreamento = Column(String(500))  # URL base para rastreamento
    api_rastreamento_url = Column(String(500))  # URL da API de rastreamento
    api_rastreamento_key = Column(String(200))  # Chave de API
    
    # =========================================================================
    # ESTATÍSTICAS
    # =========================================================================
    total_entregas_realizadas = Column(Integer, default=0)
    total_entregas_no_prazo = Column(Integer, default=0)
    total_entregas_atrasadas = Column(Integer, default=0)
    total_entregas_falhadas = Column(Integer, default=0)
    
    # =========================================================================
    # AVALIAÇÃO
    # =========================================================================
    avaliacao_media = Column(Numeric(3, 2), default=0)  # De 0 a 5
    nota_pontualidade = Column(Numeric(3, 2), default=0)
    nota_qualidade = Column(Numeric(3, 2), default=0)
    nota_atendimento = Column(Numeric(3, 2), default=0)
    
    # =========================================================================
    # STATUS
    # =========================================================================
    ativa = Column(Boolean, default=True, nullable=False, index=True)
    bloqueada = Column(Boolean, default=False, index=True)  # Bloqueada para novas entregas
    motivo_bloqueio = Column(Text)
    
    # =========================================================================
    # OBSERVAÇÕES
    # =========================================================================
    observacoes = Column(Text)
    restricoes = Column(Text)  # Restrições de entrega (ex: não entrega em finais de semana)
    
    # =========================================================================
    # DOCUMENTOS
    # =========================================================================
    documentos = Column(JSONB, default=[])
    # [
    #   {
    #     "tipo": "contrato",
    #     "nome": "Contrato de Prestação de Serviços.pdf",
    #     "url": "https://...",
    #     "data_upload": "2024-11-26T10:00:00Z"
    #   }
    # ]
    
    # =========================================================================
    # METADATA E AUDITORIA
    # =========================================================================
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    atualizado_por_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Transportadora {self.nome} - {self.cnpj}>"
    
    @property
    def disponivel(self) -> bool:
        """Verifica se a transportadora está disponível para uso"""
        return self.ativa and not self.bloqueada
    
    @property
    def taxa_entrega_no_prazo(self) -> float:
        """Calcula taxa de entregas no prazo (%)"""
        if self.total_entregas_realizadas == 0:
            return 0.0
        
        return (self.total_entregas_no_prazo / self.total_entregas_realizadas) * 100
    
    @property
    def cnpj_formatado(self) -> str:
        """Retorna CNPJ formatado"""
        if not self.cnpj:
            return ""
        
        cnpj = self.cnpj
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    def calcular_frete(self, peso_kg: float, regiao: str = None) -> float:
        """
        Calcula o valor do frete baseado no peso
        
        Args:
            peso_kg: Peso da carga em quilogramas
            regiao: Região de entrega (opcional)
        
        Returns:
            Valor do frete calculado
        """
        if self.tabela_frete and isinstance(self.tabela_frete, list):
            # Usar tabela de frete detalhada
            for faixa in self.tabela_frete:
                peso_inicial = faixa.get('faixa_peso_inicial', 0)
                peso_final = faixa.get('faixa_peso_final', float('inf'))
                
                if peso_inicial <= peso_kg <= peso_final:
                    valor_kg = faixa.get('valor_kg', 0)
                    valor_fixo = faixa.get('valor_fixo', 0)
                    return (peso_kg * valor_kg) + valor_fixo
        
        # Cálculo simples
        valor = 0
        
        if self.custo_por_kg:
            valor += peso_kg * float(self.custo_por_kg)
        
        if self.custo_por_entrega:
            valor += float(self.custo_por_entrega)
        
        # Garantir valor mínimo
        if self.valor_minimo_frete and valor < float(self.valor_minimo_frete):
            valor = float(self.valor_minimo_frete)
        
        return valor
    
    def atende_regiao(self, cidade: str, estado: str = None) -> bool:
        """
        Verifica se a transportadora atende determinada região
        
        Args:
            cidade: Nome da cidade
            estado: Sigla do estado (opcional)
        
        Returns:
            True se atende a região
        """
        if not self.cidades_atendidas:
            return False
        
        for cidade_atendida in self.cidades_atendidas:
            if isinstance(cidade_atendida, dict):
                cidade_match = cidade_atendida.get('cidade', '').lower() == cidade.lower()
                
                if estado:
                    estado_match = cidade_atendida.get('estado', '').lower() == estado.lower()
                    if cidade_match and estado_match:
                        return True
                elif cidade_match:
                    return True
        
        return False
