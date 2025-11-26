"""
Configurações centralizadas da aplicação usando Pydantic Settings.
Carrega variáveis de ambiente e fornece validação.
"""

from typing import List, Optional
from pydantic import EmailStr, validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Locnos API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Sistema de Gestão para Locadoras de Equipamentos"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str
    
    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 dias
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 dias
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            # Remove espaços e brackets se existirem
            v = v.strip()
            if v.startswith('[') and v.endswith(']'):
                v = v[1:-1]
            # Split por vírgula e limpa
            return [origin.strip().strip('"').strip("'") for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return []
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Storage
    STORAGE_BUCKET: str = "equipamentos"
    USE_SUPABASE_STORAGE: bool = True
    
    # Mercado Pago
    MERCADOPAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADOPAGO_PUBLIC_KEY: Optional[str] = None
    MERCADOPAGO_WEBHOOK_SECRET: Optional[str] = None
    
    # NF-e / NFS-e
    ENOTAS_API_KEY: Optional[str] = None
    ENOTAS_COMPANY_ID: Optional[str] = None
    ENOTAS_ENABLED: bool = False
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE: Optional[str] = None
    
    # Logs
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # First Superuser (criado no seed)
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@locnos.com.br"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    FIRST_SUPERUSER_NAME: str = "Super Admin"
    
    # Multi-tenancy
    DEFAULT_TENANT: str = "locnos"
    ENABLE_MULTI_TENANT: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()
