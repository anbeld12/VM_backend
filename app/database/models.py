from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.config import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    INVESTIGADOR = "investigador"
    REVISOR = "revisor"
    COORDINADOR = "coordinador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.INVESTIGADOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    media_source = Column(String, nullable=False) # El medio (ej. El Tiempo, El Espectador)
    published_date = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con el análisis cualitativo
    analysis = relationship("Analysis", back_populates="news", uselist=False)

class AnalysisStatus(str, enum.Enum):
    PENDING = "pendiente"
    IN_PROGRESS = "en_progreso"
    COMPLETED = "completado"

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"), unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Campos estructurados solicitados en el diseño
    structured_data = Column(JSON) # Aquí guardaremos el JSON del análisis
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    news = relationship("News", back_populates="analysis")
    investigator = relationship("User")