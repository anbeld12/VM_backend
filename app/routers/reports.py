from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Dict
import io
import csv
from datetime import datetime

from app.database.config import get_db
from app.database import models
from app.core.auth import get_current_user, RoleChecker
from app.database.models import RoleEnum, AnalysisStatus

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

# Dependencias de seguridad
require_auth = Depends(get_current_user)
require_admin_or_revisor = RoleChecker([RoleEnum.ADMIN, RoleEnum.REVISOR])

@router.get("/stats/enfoque", response_model=Dict[str, int])
def get_stats_enfoque(db: Session = Depends(get_db), current_user=require_auth):
    """
    Distribución de noticias analizadas por enfoque.
    """
    results = db.query(
        models.Analysis.enfoque, 
        func.count(models.Analysis.id)
    ).filter(
        models.Analysis.status == AnalysisStatus.COMPLETED
    ).group_by(models.Analysis.enfoque).all()
    
    return {str(enfoque.value if enfoque else "Sin Enfoque"): count for enfoque, count in results}

@router.get("/stats/media-impact", response_model=Dict[str, int])
def get_stats_media_impact(db: Session = Depends(get_db), current_user=require_auth):
    """
    Cantidad de noticias analizadas agrupadas por fuente de medio.
    """
    results = db.query(
        models.News.media_source,
        func.count(models.Analysis.id)
    ).join(models.Analysis).filter(
        models.Analysis.status == AnalysisStatus.COMPLETED
    ).group_by(models.News.media_source).all()
    
    return {media: count for media, count in results}

@router.get("/stats/top-actors", response_model=List[Dict])
def get_top_actors(db: Session = Depends(get_db), current_user=require_auth):
    """
    Los 5 actores involucrados más mencionados.
    Usa func.unnest para procesar los arrays de Postgres.
    """
    # SQL: SELECT unnest(actor_involucrado) as actor, count(*) as count 
    # FROM analysis WHERE status = 'COMPLETED' GROUP BY actor ORDER BY count DESC LIMIT 5
    
    actor_unnest = func.unnest(models.Analysis.actor_involucrado).label("actor")
    query = select(
        actor_unnest,
        func.count().label("count")
    ).where(
        models.Analysis.status == AnalysisStatus.COMPLETED
    ).group_by("actor").order_by(func.count().desc()).limit(5)
    
    results = db.execute(query).all()
    return [{"actor": r.actor, "count": r.count} for r in results]

@router.get("/export/csv")
def export_analysis_csv(db: Session = Depends(get_db), current_user=Depends(require_admin_or_revisor)):
    """
    Genera un CSV con todos los análisis completados.
    Usa StreamingResponse para eficiencia de memoria.
    """
    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Cabecera
        writer.writerow([
            "news_title", "url", "media_source", "enfoque", 
            "actores", "fecha_analisis", "investigador_nombre"
        ])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        
        # Datos (descarga perezosa de la DB si es necesario, aquí usamos query normal)
        # Para archivos MUY grandes se recomienda usar windowed query o stream_results
        analyses = db.query(models.Analysis).filter(
            models.Analysis.status == AnalysisStatus.COMPLETED
        ).all()
        
        for ana in analyses:
            writer.writerow([
                ana.news.title,
                ana.news.url,
                ana.news.media_source,
                ana.enfoque.value if ana.enfoque else "",
                ", ".join(ana.actor_involucrado) if ana.actor_involucrado else "",
                ana.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ana.investigator.nombre_completo if ana.investigator else "Desconocido"
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = f"reporte_analisis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
