from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List
from app.database.config import get_db
from app.database.models import User, RoleEnum
from app.core import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
        return current_user

# Dependencias preconfiguradas para uso en routers
require_admin = RoleChecker([RoleEnum.ADMIN])
require_analyst = RoleChecker([RoleEnum.ADMIN, RoleEnum.REVISOR, RoleEnum.INVESTIGADOR])
require_reader = RoleChecker([
    RoleEnum.ADMIN, 
    RoleEnum.REVISOR, 
    RoleEnum.INVESTIGADOR, 
    RoleEnum.TECNICO, 
    RoleEnum.LECTOR
])