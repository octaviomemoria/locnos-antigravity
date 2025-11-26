"""
Script para criar tabelas no banco de dados Supabase.
Executa: python -m app.db_init
"""

from app.core.database import Base, engine, init_db
from app.models import User, Equipment, Category, Person, Subcategoria

def create_tables():
    """Criar todas as tabelas no banco"""
    print("🗄️  Criando tabelas no banco de dados...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        print("\nTabelas criadas:")
        print("  - usuarios")
        print("  - equipamentos")
        print("  - categorias")
        print("  - subcategorias")
        print("  - pessoas")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise

if __name__ == "__main__":
    create_tables()
