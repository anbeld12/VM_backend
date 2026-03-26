from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.config import get_db
from app.database import models
from app.schemas import NewsRead, AnalysisCreate, AnalysisRead, AnalysisStats
from app.core.auth import get_current_user, RoleChecker
from app.database.models import RoleEnum

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

# Dependencia para INVESTIGADOR, REVISOR o ADMIN
require_analysis_privileges = RoleChecker([RoleEnum.INVESTIGADOR, RoleEnum.REVISOR, RoleEnum.ADMIN])

@router.get("/pending", response_model=List[NewsRead])
def get_pending_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Lista paginada de noticias que NO tienen análisis, o cuyo análisis tiene el estado 'PENDING'.
    Seguridad: Cualquier rol autenticado.
    """
    query = db.query(models.News).outerjoin(models.Analysis).filter(
        (models.Analysis.id == None) | (models.Analysis.status == models.AnalysisStatus.PENDING)
    ).order_by(models.News.scraped_at.desc()).offset(skip).limit(limit)
    
    return query.all()

@router.post("/{news_id}", response_model=AnalysisRead)
def create_or_update_analysis(
    news_id: int,
    analysis_data: AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_analysis_privileges)
):
    """
    Crea o actualiza el análisis de una noticia.
    - Si la noticia no existe: 404.
    - Si ya existe y está 'COMPLETED': 409.
    - Cambia el estado a 'COMPLETED' y asigna el user_id.
    Seguridad: INVESTIGADOR, REVISOR o ADMIN.
    """
    # 1. Validar existencia de la noticia
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")
        
    # 2. Buscar análisis existente
    analysis = db.query(models.Analysis).filter(models.Analysis.news_id == news_id).first()
    
    if analysis and analysis.status == models.AnalysisStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="La noticia ya tiene un análisis completado"
        )
    
    # 3. Preparar datos (forzando COMPLETED y user_id)
    analysis_dict = analysis_data.model_dump()
    analysis_dict["status"] = models.AnalysisStatus.COMPLETED
    analysis_dict["user_id"] = current_user.id
    
    if analysis:
        # Actualizar existente
        for key, value in analysis_dict.items():
            setattr(analysis, key, value)
        db.commit()
        db.refresh(analysis)
        return analysis
    else:
        # Crear nuevo
        new_analysis = models.Analysis(
            news_id=news_id,
            **analysis_dict
        )
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        return new_analysis

@router.get("/stats", response_model=AnalysisStats)
def get_analysis_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Resumen rápido: {"analyzed": int, "pending": int, "total": int}
    Seguridad: Cualquier rol autenticado.
    """
    total = db.query(func.count(models.News.id)).scalar()
    
    analyzed = db.query(func.count(models.Analysis.id)).filter(
        models.Analysis.status == models.AnalysisStatus.COMPLETED
    ).scalar()
    
    # Pendientes = (News sin Analysis) + (Analysis con status PENDING)
    news_without_analysis = db.query(func.count(models.News.id)).outerjoin(models.Analysis).filter(
        models.Analysis.id == None
    ).scalar()
    
    analysis_pending = db.query(func.count(models.Analysis.id)).filter(
        models.Analysis.status == models.AnalysisStatus.PENDING
    ).scalar()
    
    return {
        "analyzed": analyzed,
        "pending": news_without_analysis + analysis_pending,
        "total": total
    }
