"""
Aplicação principal FastAPI - Locnos
Sistema de Gestão para Locadoras de Equipamentos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.core.config import settings

# Criar instância do FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENDPOINTS BÁSICOS
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raiz - redireciona para docs"""
    return {
        "message": "Bem-vindo à API Locnos!",
        "docs": "/docs",
        "version": settings.VERSION,
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check - verifica se a API está online"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/health")
async def api_health_check():
    """Health check alternativo - compatível com Render"""
    return await health_check()



@app.get(f"{settings.API_V1_STR}/test")
async def test_endpoint():
    """Endpoint de teste"""
    return {
        "message": "API FastAPI funcionando perfeitamente! 🚀",
        "framework": "FastAPI",
        "language": "Python 3.11+",
        "database": "Supabase (PostgreSQL)",
        "features": [
            "Tipagem forte com Pydantic",
            "Documentação automática (Swagger)",
            "Performance async",
            "Multi-tenancy preparado"
        ]
    }


# ============================================================================
# EVENT HANDLERS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Executado quando a aplicação inicia"""
    print("=" * 60)
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📍 Ambiente: {settings.ENVIRONMENT}")
    print(f"🌐 Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Executado quando a aplicação encerra"""
    print("\n👋 Encerrando aplicação...")


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handler personalizado para 404"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"Rota {request.url.path} não encontrada",
            "docs": "/docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handler para erros internos"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "detail": str(exc) if settings.DEBUG else "Erro inesperado"
        }
    )


# ============================================================================
# INCLUIR ROUTERS
# ============================================================================

from app.api.v1 import auth_router, equipment_router, persons_router, subcategorias_router, dashboard_router

app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Autenticação"]
)

app.include_router(
    equipment_router,
    prefix=f"{settings.API_V1_STR}/equipment",
    tags=["Equipamentos"]
)

app.include_router(
    persons_router,
    prefix=f"{settings.API_V1_STR}/persons",
    tags=["Pessoas"]
)

app.include_router(
    subcategorias_router,
    prefix=f"{settings.API_V1_STR}/subcategorias",
    tags=["Subcategorias"]
)

app.include_router(
    dashboard_router,
    prefix=f"{settings.API_V1_STR}/dashboard",
    tags=["Dashboard"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
