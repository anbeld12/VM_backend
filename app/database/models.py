from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from app.database.config import Base
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    INVESTIGADOR = "INVESTIGADOR"
    REVISOR = "REVISOR"
    TECNICO = "TECNICO"
    LECTOR = "LECTOR"

class AnalysisStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class EnfoqueEnum(str, enum.Enum):
    Paz = "Paz"
    Conflicto = "Conflicto"
    Memoria = "Memoria"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False, default='Usuario V&M')
    role = Column(Enum(RoleEnum), default=RoleEnum.LECTOR, nullable=False)
    is_active = Column(Boolean, default=True)
    ultimo_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    media_source = Column(String, nullable=False) # El medio (ej. El Tiempo, El Espectador)
    autor = Column(String, nullable=True)
    published_date = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con el análisis cualitativo
    analysis = relationship("Analysis", back_populates="news", uselist=False)

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"), unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Campos estructurados nativos
    enfoque = Column(Enum(EnfoqueEnum), nullable=True)
    actor_involucrado = Column(ARRAY(String), nullable=True)
    tipo_violencia = Column(ARRAY(String), nullable=True)
    etiquetas_adicionales = Column(ARRAY(String), nullable=True)
    observaciones = Column(Text, nullable=True)
    
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    news = relationship("News", back_populates="analysis")
    investigator = relationship("User")