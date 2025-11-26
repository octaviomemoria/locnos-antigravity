"""
Dependencies para autenticação e autorização
Usado como Depends() nos endpoints FastAPI
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole
from app.schemas.auth import TokenPayload


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obter usuário autenticado via JWT token.
    Uso: current_user: User = Depends(get_current_user)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para garantir que usuário está ativo.
    Uso: current_user: User = Depends(get_current_active_user)
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    return current_user


def require_role(*allowed_roles: UserRole):
    """
    Factory para criar dependency que verifica roles.
    Uso: admin_user: User = Depends(require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN))
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer role: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    return role_checker


def require_permission(permission: str):
    """
    Factory para criar dependency que verifica permissões específicas.
    Uso: user: User = Depends(require_permission('manage_equipment'))
    """
    async def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if permission not in current_user.permissions and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão negada. Requer: {permission}"
            )
        return current_user
    return permission_checker


# Atalhos para roles comuns
require_admin = require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN)
require_staff = require_role(UserRole.STAFF, UserRole.ADMIN, UserRole.SUPER_ADMIN)
