from fastapi import FastAPI
from app.database.config import engine, Base
from app.database import models

# Esto crea las tablas si no existen al iniciar la app
# Aquí es donde realmente se usa el metadata, no se importa
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Observatorio V&M",
    description="Backend para el Sistema de Monitoreo Automatizado de Medios",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensaje": "API del Observatorio V&M con Base de Datos conectada y funcionando"}