from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr
from app.database.models import RoleEnum, EnfoqueEnum, AnalysisStatus
from datetime import datetime

# Esquema para el Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Esquemas de Usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr
    nombre_completo: str
    role: RoleEnum = RoleEnum.LECTOR

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    ultimo_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Alias para mantener compatibilidad si es necesario (opcional, pero sugerido si se usa UserOut en otros lados)
UserOut = UserRead

class NewsBase(BaseModel):
    title: str
    url: str
    media_source: str
    published_date: Optional[datetime] = None

class NewsOut(NewsBase):
    id: int
    scraped_at: datetime

    class Config:
        from_attributes = True

NewsRead = NewsOut

# Schemas de Análisis Cualitativo
class AnalysisCreate(BaseModel):
    enfoque: EnfoqueEnum
    actor_involucrado: List[str]
    tipo_violencia: List[str]
    etiquetas_adicionales: Optional[List[str]] = []
    observaciones: Optional[str] = None

class AnalysisRead(AnalysisCreate):
    id: int
    news_id: int
    user_id: int
    status: AnalysisStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnalysisStats(BaseModel):
    analyzed: int
    pending: int
    total: int