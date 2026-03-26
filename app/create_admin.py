from app.database.config import SessionLocal
from app.database.models import User, UserRole
from app.core.security import get_password_hash

def create_first_admin():
    db = SessionLocal()
    admin_exists = db.query(User).filter(User.username == "admin").first()
    
    if not admin_exists:
        admin_user = User(
            username="admin",
            email="admin@observatoriovm.org",
            hashed_password=get_password_hash("admin123"), # Cambia esto luego
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Usuario Administrador creado: admin / admin123")
    else:
        print("ℹ️ El administrador ya existe.")
    db.close()

if __name__ == "__main__":
    create_first_admin()