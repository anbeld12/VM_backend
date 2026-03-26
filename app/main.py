from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.config import engine, Base, get_db
from app.database import models
from app import schemas
from app.core import security, auth
from typing import List
from app.schemas import NewsOut
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Observatorio V&M", version="1.0.0")

@app.post("/auth/login", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/")
def read_root():
    return {"mensaje": "API del Observatorio V&M funcionando"}

@app.get("/news", response_model=List[NewsOut])
def get_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Obtiene las noticias recolectadas por el scraper.
    """
    news = db.query(models.News).order_by(models.News.scraped_at.desc()).offset(skip).limit(limit).all()
    return news