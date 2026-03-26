import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Recreamos el modelo News para que el Scraper sepa cómo es la tabla
class NewsModel(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    media_source = Column(String, nullable=False)
    published_date = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

class ObservatorioScraperPipeline:
    def __init__(self):
        # Conectamos a la base de datos usando la variable de entorno de Docker
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:vm_admin123@db:5432/observatorio_vm")
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            # 1. Verificar si la noticia ya existe en la base de datos (por URL)
            existe = session.query(NewsModel).filter_by(url=item['url']).first()
            
            if not existe:
                # 2. Si no existe, preparamos el objeto para guardarlo
                nueva_noticia = NewsModel(
                    title=item['titulo'],
                    content=item['contenido'],
                    url=item['url'],
                    media_source=item['fuente']
                    # La fecha de publicación requiere un parseo avanzado según cada medio,
                    # por ahora la dejaremos nula y registraremos la fecha de scraping.
                )
                session.add(nueva_noticia)
                session.commit()
                spider.logger.info(f"✅ Noticia guardada: {item['titulo']}")
            else:
                spider.logger.debug(f"⚠️ Noticia duplicada ignorada: {item['titulo']}")
                
        except Exception as e:
            session.rollback()
            spider.logger.error(f"❌ Error al guardar en BD: {e}")
        finally:
            session.close()
            
        return item