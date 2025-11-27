# Facilita imports dos routers
from .auth import router as auth_router
from .equipment import router as equipment_router
from .persons import router as persons_router
from .subcategorias import router as subcategorias_router
from .dashboard import router as dashboard_router

__all__ = ["auth_router", "equipment_router", "persons_router", "subcategorias_router", "dashboard_router"]
