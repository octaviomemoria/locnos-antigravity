"""
Script para criar tabelas de contratos no banco de dados
Execute: python -m app.create_contract_tables
"""

from app.core.database import engine, Base
from app.models import Contract, ContractItem, ContractStatus

def create_tables():
    """Cria as tabelas de contratos no banco"""
    print("🔨 Criando tabelas de contratos...")
    
    try:
        # Criar apenas as tabelas de Contract e ContractItem
        Contract.__table__.create(engine, checkfirst=True)
        ContractItem.__table__.create(engine, checkfirst=True)
        
        print("✅ Tabelas criadas com sucesso!")
        print("   - contratos")
        print("   - itens_contrato")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise

if __name__ == "__main__":
    create_tables()
