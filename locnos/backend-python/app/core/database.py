"""
Configuração do banco de dados SQLAlchemy com Supabase (PostgreSQL).
Suporte a multi-tenancy com schemas separados.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .config import settings

import logging

logger = logging.getLogger(__name__)

# Engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool if settings.ENVIRONMENT == "test" else None,
    echo=settings.DEBUG,  # Log SQL queries em development
    pool_pre_ping=True,  # Verificar conexão antes de usar
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados.
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tabelas do banco de dados criadas/verificadas")


# Event listener para logging de queries (apenas em debug)
if settings.DEBUG:
    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        logger.debug(f"SQL: {statement}")
        logger.debug(f"Params: {params}")
