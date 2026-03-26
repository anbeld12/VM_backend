from pydantic import BaseModel, EmailStr
from typing import Optional
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