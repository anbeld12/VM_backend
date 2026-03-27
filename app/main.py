from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.config import engine, Base, get_db
from app.database import models
from app import schemas
from app.core import security, auth
from typing import List
from app.schemas import NewsOut
from app.routers import analysis, reports
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Observatorio V&M", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(reports.router)

@app.post("/auth/login", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Aceptamos login por username o email para alinearnos con el frontend.
    user = db.query(models.User).filter(
        (models.User.username == form_data.username) | (models.User.email == form_data.username)
    ).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=schemas.UserOut)
def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    """
    Crea un nuevo usuario. Solo accesible por ADMIN.
    """
    if db.query(models.User).filter(
        (models.User.username == user_data.username) | (models.User.email == user_data.email)
    ).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario o email ya existe")
    
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        nombre_completo=user_data.nombre_completo,
        hashed_password=security.get_password_hash(user_data.password),
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/")
def read_root():
    return {"mensaje": "API del Observatorio V&M funcionando"}

@app.get("/news", response_model=List[NewsOut])
def get_news(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Obtiene las noticias recolectadas por el scraper. Requiere autenticación.
    """
    news = db.query(models.News).order_by(models.News.scraped_at.desc()).offset(skip).limit(limit).all()
    return news