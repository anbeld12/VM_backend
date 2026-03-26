from typing import Optional, List, Literal, Any, Dict
from pydantic import BaseModel, EmailStr, Field
from app.database.models import UserRole
from datetime import datetime

# Esquema para el Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Esquema para mostrar datos de usuario
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

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

# Schemas de Análisis Cualitativo
class StructuredData(BaseModel):
    actor_involucrado: List[str]
    tipo_violencia: List[str]
    enfoque: Literal["Paz", "Conflicto", "Memoria"]
    etiquetas_adicionales: List[str] = Field(default_factory=list)
    observaciones: str

class AnalysisCreate(BaseModel):
    structured_data: StructuredData

class AnalysisRead(BaseModel):
    id: int
    news_id: int
    user_id: int
    status: Any
    structured_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnalysisStats(BaseModel):
    analyzed: int
    pending: int
    total: int