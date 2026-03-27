import os
from app.database.config import SessionLocal
from app.database.models import User, RoleEnum
from app.core.security import get_password_hash

def create_first_admin():
    # Obtener contraseña del admin desde variables de entorno
    admin_password = os.getenv("INITIAL_ADMIN_PASSWORD")
    if not admin_password:
        raise ValueError(
            "ERROR CRÍTICO: INITIAL_ADMIN_PASSWORD no está definida en variables de entorno.\n"
            "Establece una contraseña segura en tu archivo .env."
        )
    
    db = SessionLocal()
    admin_exists = db.query(User).filter(User.username == "admin").first()
    
    if not admin_exists:
        admin_user = User(
            username="admin",
            email="admin@observatoriovm.org",
            nombre_completo="Administrador Sistema",
            hashed_password=get_password_hash(admin_password),
            role=RoleEnum.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Usuario Administrador creado exitosamente")
        print("⚠️  IMPORTANTE: Cambia la contraseña en tu primera sesión")
    else:
        print("ℹ️ El administrador ya existe.")
    db.close()

if __name__ == "__main__":
    create_first_admin()