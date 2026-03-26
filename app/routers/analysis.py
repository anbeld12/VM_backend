from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.config import get_db
from app.database import models
from app.schemas import NewsOut, AnalysisCreate, AnalysisRead, AnalysisStats
from app.core.auth import get_current_user, require_analyst

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
    responses={404: {"description": "No encontrado"}},
)

@router.get("/news/pending-analysis", response_model=List[NewsOut], tags=["News"])
def get_pending_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtiene las noticias recolectadas que NO tienen un análisis o cuyo status sea 'PENDING'.
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
    current_user: models.User = Depends(require_analyst)
):
    """
    Crea o actualiza un análisis para una noticia específica.
    """
    # Validar que la noticia existe
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
        
    analysis = db.query(models.Analysis).filter(models.Analysis.news_id == news_id).first()
    
    analysis_dict = analysis_data.model_dump()
    analysis_dict["status"] = models.AnalysisStatus.COMPLETED
    analysis_dict["user_id"] = current_user.id
    
    if analysis:
        # Validar si ya está siendo analizada de forma no PENDING
        if analysis.status != models.AnalysisStatus.PENDING:
            raise HTTPException(
                status_code=409, 
                detail="La noticia ya ha sido analizada o está en proceso de análisis por otro investigador"
            )
        
        # Update existing analysis
        for key, value in analysis_dict.items():
            setattr(analysis, key, value)
        
        db.commit()
        db.refresh(analysis)
        return analysis
    else:
        # Create new analysis
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
    Un resumen rápido que devuelve estadísticas de noticias.
    """
    total_news = db.query(func.count(models.News.id)).scalar()
    
    analyzed_news = db.query(func.count(models.Analysis.id)).filter(
        models.Analysis.status == models.AnalysisStatus.COMPLETED
    ).scalar()
    
    pending_analysis = db.query(func.count(models.Analysis.id)).filter(
        models.Analysis.status == models.AnalysisStatus.PENDING
    ).scalar()
    
    news_without_analysis = db.query(func.count(models.News.id)).outerjoin(models.Analysis).filter(
        models.Analysis.id == None
    ).scalar()
    
    pending_total = pending_analysis + news_without_analysis
    
    return {
        "analyzed": analyzed_news,
        "pending": pending_total,
        "total": total_news
    }
