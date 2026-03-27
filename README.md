# 🚀 Observatorio V&M - Backend

API REST FastAPI para la plataforma de clasificación cualitativa de artículos noticiosos sobre el Proceso de Paz y el Conflicto Armado Colombiano. Incluye sistema de scraping web con Scrapy y base de datos PostgreSQL.

![Estado](https://img.shields.io/badge/status-en%20desarrollo-yellow?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10-3776ab?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)

---

## 📋 Tabla de Contenidos

1. [Descripción](#descripción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Rápida](#instalación-rápida)
4. [Variables de Entorno](#variables-de-entorno)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Ejecución en Desarrollo](#ejecución-en-desarrollo)
7. [Base de Datos & Migraciones](#base-de-datos--migraciones)
8. [API Endpoints](#api-endpoints)
9. [Autenticación JWT](#autenticación-jwt)
10. [Web Scraper](#web-scraper)
11. [Docker & Deployment](#docker--deployment)
12. [Seguridad](#seguridad)
13. [Troubleshooting](#troubleshooting)
14. [Contribuciones](#contribuciones)

---

## 📖 Descripción

El **Backend de Observatorio V&M** es una API REST construida con **FastAPI** que proporciona:

### Funcionalidades

- 🔐 **Autenticación JWT** con control de acceso basado en roles (RBAC)
- 📰 **API de Noticias** para gestionar artículos y metadata
- 📊 **API de Análisis** para clasificación cualitativa
- 📈 **API de Reportes** con estadísticas y tendencias
- 👥 **Gestión de Usuarios** con diferentes roles
- 🕷️ **Web Scraper** automático con Scrapy (17 fuentes de noticias)
- 🗄️ **Base de Datos PostgreSQL** con migraciones Alembic
- 🔄 **Cache Redis** para optimización
- 📚 **Documentación OpenAPI** interactiva (Swagger UI)

### Características Técnicas

- ✅ Autenticación OAuth2 con JWT
- ✅ Validación de datos con Pydantic
- ✅ ORM SQLAlchemy con SQLModel
- ✅ Migraciones automáticas con Alembic
- ✅ CORS configurable por entorno
- ✅ Logging estructurado
- ✅ Dockerizado con docker-compose
- ✅ Variables de entorno seguras

---

## 🛠️ Requisitos Previos

### Opción 1: Desarrollo Local

- **Python** `>= 3.10`
- **PostgreSQL** `>= 15` (local o Docker)
- **Redis** `>= 7` (local o Docker)
- **pip** o **poetry** para gestionar dependencias
- **git** para control de versiones

**Verificar versiones:**
```bash
python --version   # Debe ser 3.10+
pip --version      # Debe funcionar
psql --version     # Si está instalado localmente
```

### Opción 2: Docker (Recomendado)

- **Docker** `>= 20.10`
- **Docker Compose** `>= 2.0`

**Verificar instalación:**
```bash
docker --version
docker-compose --version
```

---

## 📦 Instalación Rápida

### Opción A: With Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone <url-del-repositorio>
cd V\&M/VM_backend

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Editar .env con valores locales (opcional, .env.example tiene defaults)
nano .env

# 4. Levantardockercontainers
docker-compose up -d

# 5. Verificar que esté corriendo
docker-compose ps

# 6. Ver logs
docker-compose logs -f api

# 7. Crear usuario admin
docker exec vm_api python app/create_admin.py
```

**API estará en:** http://localhost:8000  
**Docs en:** http://localhost:8000/docs

---

### Opción B: Desarrollo Local (Python)

```bash
# 1. Clonar repositorio
git clone <url-del-repositorio>
cd V\&M/VM_backend

# 2. Crear ambiente virtual
python -m venv venv

# 3. Activar ambiente
# En macOS/Linux:
source venv/bin/activate

# En Windows:
.\venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Copiar variables de entorno
cp .env.example .env

# 6. Editar .env para apuntar a BD local
# DATABASE_URL=postgresql://user:password@localhost/observatorio_vm
nano .env

# 7. Iniciar PostgreSQL (si lo tienes instalado)
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# 8. Crear base de datos
createdb observatorio_vm

# 9. Ejecutar migraciones
alembic upgrade head

# 10. Crear usuario admin
python app/create_admin.py

# 11. Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔐 Variables de Entorno

El backend requiere las siguientes variables configuradas en `.env`.

### Variables Obligatorias

```env
# ========== BASE DE DATOS ==========
# Usuario PostgreSQL
POSTGRES_USER=postgres

# Contraseña PostgreSQL (CAMBIAR EN PRODUCCIÓN)
POSTGRES_PASSWORD=tu_contraseña_segura

# Nombre de la base de datos
POSTGRES_DB=observatorio_vm

# URL de conexión (construida automáticamente por Docker)
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

# ========== SEGURIDAD JWT ==========
# Clave secreta para firmar JWT
# Generar con: openssl rand -hex 32
# IMPORTANTE: Debe tener 64 caracteres hexadecimales
JWT_SECRET_KEY=<generar_con_openssl>

# Contraseña inicial del usuario administrador
# Se usa una sola vez al crear el admin
# Cambiar en producción
INITIAL_ADMIN_PASSWORD=tu_contraseña_inicial

# ========== REDIS (OPCIONAL) ==========
REDIS_URL=redis://redis:6379/0

# ========== CORS ==========
# Orígenes permitidos para CORS (separados por comas)
# Desarrollo:
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Producción:
# CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com

# ========== ENTORNO ==========
ENVIRONMENT=development  # o: staging, production
```

### Ejemplo Completo de .env

Ver archivo [.env.example](.env.example) para referencia completa.

### 🚨 IMPORTANTE - Seguridad

`⚠️ NUNCA commitar .env con credenciales reales a Git`

- `.env` está en `.gitignore`
- Solo `.env.example` debe estar en Git
- Generar claves seguras para producción:
  ```bash
  # JWT Secret
  openssl rand -hex 32
  
  # Database Password
  openssl rand -base64 16
  ```
- En producción, usar Secrets Manager (AWS Secrets, Vault, etc.)

---

## 📂 Estructura del Proyecto

```
VM_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                       # Aplicación FastAPI principal
│   │                                 # - Configuración de CORS
│   │                                 # - Routers incluidos
│   │                                 # - Eventos de startup
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py                   # Dependencias de autorización
│   │   │                             # - get_current_user()
│   │   │                             # - RoleChecker
│   │   │                             # - require_admin, require_analyst
│   │   │
│   │   └── security.py               # Funciones de seguridad
│   │                                 # - get_password_hash()
│   │                                 # - verify_password()
│   │                                 # - create_access_token()
│   │                                 # - JWT config: SECRET_KEY, ALGORITHM
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuración de base de datos
│   │   │                             # - engine: SQLAlchemy engine
│   │   │                             # - SessionLocal: Session factory
│   │   │                             # - get_db(): Dependency para sesiones
│   │   │
│   │   └── models.py                 # Modelos SQLAlchemy/SQLModel
│   │                                 # - User (con roles, email, password_hash)
│   │                                 # - News (artículos scrapeados)
│   │                                 # - Analysis (análisis de usuarios)
│   │                                 # - Report (reportes generados)
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analysis.py               # Endpoints: /analysis/*
│   │   │                             # - GET /analysis
│   │   │                             # - POST /analysis
│   │   │                             # - PUT /analysis/{id}
│   │   │
│   │   └── reports.py                # Endpoints: /reports/*
│   │                                 # - GET /reports
│   │                                 # - GET /reports/{id}
│   │                                 # - POST /reports
│   │
│   ├── schemas.py                    # Schemas Pydantic para validación
│   │                                 # - UserCreate, UserOut
│   │                                 # - NewsOut
│   │                                 # - Token
│   │                                 # - AnalysisCreate, AnalysisOut
│   │
│   └── create_admin.py               # Script para crear usuario admin
│                                     # Ejecutar: python app/create_admin.py
│
├── alembic/                          # Migraciones de base de datos
│   ├── env.py                        # Script de migración
│   ├── script.py.mako                # Template para nuevas migraciones
│   └── versions/                     # Archivos de versiones (.py)
│
├── vm_scraper/
│   ├── launcher.py                   # Script para iniciar spiders
│   ├── scrapy.cfg                    # Configuración de Scrapy
│   └── observatorio_scraper/
│       ├── __init__.py
│       ├── settings.py               # Configuración de Scrapy
│       │                             # - ITEM_PIPELINES
│       │                             # - USER_AGENT
│       │                             # - DOWNLOAD_DELAY
│       │
│       ├── items.py                  # Definición de items a scrapear
│       ├── pipelines.py              # Procesamiento de items (guardar a BD)
│       ├── middlewares.py            # Middlewares personalizados
│       │
│       └── spiders/                  # Spiders para cada fuente
│           ├── __init__.py
│           ├── eltiempo_spider.py    # El Tiempo
│           ├── elespectador_spider.py # El Espectador
│           ├── semana_spider.py      # Semana
│           ├── lasillavacia_spider.py # La Silla Vacía
│           ├── cambio_spider.py      # Cambio
│           ├── bluradio_spider.py    # Blue Radio
│           └── ... (12 más)
│
├── .env                              # Variables de entorno (NO en Git)
├── .env.example                      # Plantilla (en Git)
├── .gitignore                        # Archivos ignorados por Git
├── requirements.txt                  # Dependencias Python
├── Dockerfile                        # Imagen Docker
├── docker-compose.yml                # Orquestación de containers
├── alembic.ini                       # Configuración de Alembic
│
├── SECURITY_AUDIT_REPORT.md          # Auditoría de seguridad
├── SECURITY_FIXES.md                 # Soluciones implementadas
├── README_AUDIT.md                   # Resumen de auditoría
├── QUICK_REFERENCE.md                # Referencia rápida
└── README.md                         # Este archivo
```

---

## 🏃 Ejecución en Desarrollo

### Con Docker (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver servicios corriendo
docker-compose ps

# Ver logs
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f redis

# Detener servicios
docker-compose down

# Limpiar volumes (cuidado: borra datos)
docker-compose down -v
```

### Sin Docker (Python Local)

```bash
# Activar ambiente virtual
source venv/bin/activate  # macOS/Linux
# o
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O con configuración de desarrollo
python -m uvicorn app.main:app --reload

# O con archivo de configuración
uvicorn app.main:app --config-path uvicorn_config.yaml
```

### Verificar que está corriendo

```bash
# En otra terminal
curl http://localhost:8000/
# Response esperado:
# {"mensaje": "API del Observatorio V&M funcionando"}

# Ver Swagger UI (documentación interactiva)
open http://localhost:8000/docs

# Ver ReDoc (documentación alternativa)
open http://localhost:8000/redoc
```

---

## 🗄️ Base de Datos & Migraciones

### Entender el Sistema de Migraciones

El proyecto usa **Alembic** para gestionar cambios en el esquema de la base de datos.

**Flujo:**

```
Cambias códigomodels.py
  ↓
Alembic detecta cambios
  ↓
Creas migración: alembic revision --autogenerate -m "descripción"
  ↓
Revisa el archivo generado en alembic/versions/
  ↓
Aplica migración: alembic upgrade head
```

### Aplicar Migraciones

```bash
# Ver estado actual
alembic current

# Ver todas las migraciones
alembic history

# Aplicar todas las pendientes
alembic upgrade head

# Aplicar una migración específica
alembic upgrade abc123def

# Revertir la última
alembic downgrade -1

# Revertir todo
alembic downgrade base
```

### Crear Nueva Migración

1. **Modificar modelo en `app/database/models.py`:**

```python
# Ej: Agregar campo a tabla User
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[Optional[str]] = mapped_column(nullable=True)  # NUEVO
    # ...
```

2. **Generar migración automática:**

```bash
alembic revision --autogenerate -m "agregar campo phone a users"
```

3. **Revisar archivo generado:**

```bash
cat alembic/versions/abc123def_agregar_campo_phone_a_users.py
```

4. **Aplicar:**

```bash
alembic upgrade head
```

### Conectar Directamente a la BD

```bash
# Con Docker
docker exec -it vm_postgres psql -U postgres -d observatorio_vm

# Localmente (si PostgreSQL instalado)
psql -U postgres -d observatorio_vm

# Queries útiles
\d users              -- Ver estructura de tabla
\d                    -- Listar todas las tablas
SELECT * FROM users;  -- Ver datos
```

---

## 📡 API Endpoints

### Documentación Interactiva

Navega a **http://localhost:8000/docs** para ver:

- ✅ Todos los endpoints
- ✅ Parámetros requeridos y opcionales
- ✅ Esquemas de request/response
- ✅ Probar endpoints directamente

### Endpoints Principales

#### Autenticación

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=tu_contraseña

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Usuarios

```http
GET /users/me
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "username": "admin",
  "email": "admin@observatoriovm.org",
  "nombre_completo": "Administrador",
  "role": "ADMIN",
  "is_active": true,
  "created_at": "2026-03-27T10:00:00"
}
```

```http
POST /users
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "nuevo_user",
  "email": "nuevo@example.com",
  "nombre_completo": "Nuevo Usuario",
  "password": "contraseña_segura",
  "role": "INVESTIGADOR"
}
```

#### Noticias

```http
GET /news
Authorization: Bearer <token>
?skip=0&limit=20

Response:
[
  {
    "id": "1",
    "title": "Titulo del articulo",
    "source": "El Tiempo",
    "original_url": "https://...",
    "published_date": "2026-03-27",
    "scraped_date": "2026-03-27T10:15:00",
    "content": "Contenido del articulo..."
  },
  ...
]
```

#### Análisis

```http
POST /analysis
Authorization: Bearer <token>
Content-Type: application/json

{
  "news_id": 1,
  "classification": "POSITIVE",
  "category": "Paz",
  "notes": "articulo importante sobre..."
}
```

#### Reportes

```http
GET /reports
Authorization: Bearer <token>

Response:
{
  "total_news": 1500,
  "news_by_status": {
    "PENDING": 500,
    "IN_PROGRESS": 700,
    "COMPLETED": 300
  },
  "news_by_source": {
    "El Tiempo": 350,
    "El Espectador": 280,
    ...
  }
}
```

---

## 🔐 Autenticación JWT

### Flow de Autenticación

```
Usuario ingresa credenciales
        ↓
Backend valida contra BD
        ↓
Genera JWT firmado con SECRET_KEY
        ↓
Frontend guarda JWT en localStorage
        ↓
Frontend envía en: Authorization: Bearer <jwt>
        ↓
Backend valida firma y expiration
        ↓
Retorna 401 si está expirado
        ↓
Frontend limpia sesión y redirige a login
```

### Estructura del JWT

```javascript
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "sub": "admin",        // username
  "exp": 1711702800,     // expiration timestamp
  "iat": 1711616400      // issued at timestamp
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)
```

### Uso en Endpoints

Los endpoints protegidos requieren:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Si falta token o es inválido → **401 Unauthorized**

### Roles y Permisos

|Endpoint|ADMIN|INVESTIGADOR|REVISOR|TECNICO|LECTOR|
|--------|-----|------------|-------|-------|------|
|GET /news|✅|✅|✅|✅|✅|
|POST /analysis|✅|✅|✅|❌|❌|
|PUT /analysis/{id}|✅|✅|✅|❌|❌|
|GET /reports|✅|✅|✅|✅|✅|
|POST /users|✅|❌|❌|❌|❌|
|DELETE /users/{id}|✅|❌|❌|❌|❌|

---

## 🕷️ Web Scraper

El proyecto incluye un **scraper automático con Scrapy** que recopila artículos de 17 fuentes de noticias.

### Fuentes Soportadas

1. El Tiempo
2. El Espectador
3. Semana
4. La Silla Vacía
5. Cambio
6. Blue Radio
7. Law
8. Noticias RCN
9. Noticias Caracol
10. Las 2 Orillas
11. Noticias Uno
12. RTVC Noticias
13. La FM
14. CMI
15. Cuestión Pública
16. El Colombiano
17. Y más...

### Ejecutar el Scraper

```bash
# Opción 1: Dentro de Docker
docker exec vm_scraper python launcher.py

# Opción 2: Localmente
cd vm_scraper
python launcher.py

# Ver opciones
python launcher.py --help

# Ejecutar spiders específicos
python launcher.py --spiders eltiempo,elespectador

# Vaciar caché de Redis (reprocess todas las URLs)
python launcher.py --flush-redis
```

### Cómo Funciona

1. **Spider se conecta** a cada sitio de noticias
2. **Extrae metadata**: título, URL, fecha, contenido
3. **Valida duplicados** en Redis (por URL)
4. **Guarda en BD** si es nuevo
5. **Registra logs** de cada artículo

### Agregar Nueva Fuente

1. Crear `vm_scraper/observatorio_scraper/spiders/mi_fuente_spider.py`:

```python
import scrapy
from ..items import NewsItem

class MiFuenteSpider(scrapy.Spider):
    name = "mi_fuente"
    allowed_domains = ["ejemplo.com"]
    start_urls = ["https://ejemplo.com/noticias"]
    
    def parse(self, response):
        for article in response.css('article.post'):
            yield NewsItem(
                titulo=article.css('.title::text').get(),
                url=article.css('a::attr(href)').get(),
                contenido=article.css('.content::text').get(),
                fuente="Mi Fuente",
            )
        
        # Paginación
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
```

2. Agregar nombre en `launcher.py`:

```python
SPIDERS = [
    "eltiempo",
    "mi_fuente",  # NUEVO
    # ...
]
```

3. Ejecutar:

```bash
python launcher.py --spiders mi_fuente
```

---

## 🐳 Docker & Deployment

### Docker Compose

El proyecto incluye `docker-compose.yml` que levanta:

- **API** (FastAPI + Uvicorn)
- **Database** (PostgreSQL 15)
- **Cache** (Redis 7)
- **Scraper** (Scrapy)

### Comandos Útiles

```bash
# Iniciar todo
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs de api
docker-compose logs -f api

# Ver logs de específico servicio
docker-compose logs -f db
docker-compose logs -f redis

# Ejecutar comando en container
docker exec vm_api python app/create_admin.py

# Detener
docker-compose down

# Limpiar volumes (CUIDADO: borra datos)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Solo levantar servicios específicos
docker-compose up -d db redis
docker-compose up api
```

### Deployment en Producción

#### 1. Preparar servidor

```bash
# Instalar Docker y Docker Compose
curl -fsSL https://get.docker.com | sh
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

#### 2. Clonar y configurar

```bash
git clone <repo> /opt/vm_backend
cd /opt/vm_backend

# Generar secretos seguros
openssl rand -hex 32  # Para JWT_SECRET_KEY
openssl rand -base64 16  # Para POSTGRES_PASSWORD

# Crear .env con valores reales
cp .env.example .env
# Editar .env con credenciales de producción
nano .env
```

#### 3. Configurar NGINX (proxy reverso)

```nginx
server {
    listen 80;
    server_name api.tudominio.com;
    
    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.tudominio.com;
    
    ssl_certificate /etc/letsencrypt/live/api.tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.tudominio.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. Levantar en producción

```bash
docker-compose -f docker-compose.yml up -d

# Verificar
curl https://api.tudominio.com/
```

#### 5. Backups

```bash
# Backup de BD
docker exec vm_postgres pg_dump -U postgres observatorio_vm > /backups/db_$(date +%Y%m%d).sql

# Restaurar
cat /backups/db_20260327.sql | docker exec -i vm_postgres psql -U postgres observatorio_vm
```

---

## 🔒 Seguridad

Este proyecto implementa múltiples capas de protección.

### ✅ Medidas Implementadas

#### 1. Credenciales Seguras

- ✅ No hay hardcoding de contraseñas
- ✅ Todas las credenciales desde variables de entorno
- ✅ Validación obligatoria de variables críticas
- ✅ Contraseña de admin desde INITIAL_ADMIN_PASSWORD

**Verificar:**
```bash
# En .env
grep "POSTGRES_PASSWORD=vm_admin123" .env && echo "❌ CAMBIAR!" || echo "✅ Safe"
grep "JWT_SECRET_KEY=" .env | grep -v "^#"
```

#### 2. Hashing de Contraseñas

- ✅ Bcrypt para hash de contraseñas (rounds=12)
- ✅ Salt incluido automáticamente
- ✅ No se almacenan contraseñas en texto plano

```python
# En security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Generar hash: pwd_context.hash("contraseña")
# Verificar: pwd_context.verify("contraseña", hash)
```

#### 3. JWT Seguro

- ✅ Firma HMAC-SHA256
- ✅ Expiración: 24 horas
- ✅ SECRET_KEY validado obligatoriamente
- ✅ Algoritmo especificado en header

#### 4. Control de Acceso

- ✅ RBAC (Role-Based Access Control)
- ✅ Validación de roles en cada endpoint
- ✅ Dependencias de FastAPI para autorización

```python
# En auth.py
class RoleChecker:
    def __init__(self, allowed_roles: List[RoleEnum]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

require_admin = RoleChecker([RoleEnum.ADMIN])
```

#### 5. CORS Protegido

- ✅ Controlado por variable `CORS_ORIGINS`
- ✅ Solo orígenes permitidos pueden acceder
- ✅ Credentials solo con HTTPS

#### 6. SQL Injection Protection

- ✅ SQLModel/SQLAlchemy ORM (parámetros escapados)
- ✅ No concatenar strings en queries
- ✅ Validación con Pydantic

#### 7. Validación de Entrada

- ✅ Pydantic schemas para todos los inputs
- ✅ Type hints en todos los parámetros
- ✅ Validadores personalizados cuando es necesario

### ⚠️ Recomendaciones Adicionales

1. **Cambiar Contraseña de Postgres en Producción**
   ```sql
   ALTER USER postgres WITH PASSWORD 'nueva_contraseña_segura';
   ```

2. **Rotación de JWT_SECRET_KEY**
   - Cambiar cada 6-12 meses
   - O cuando sospechas compromiso

3. **Logging y Monitoreo**
   - Activar logging estructurado
   - Monitorear intentos fallidos de auth
   - Alertas en errores críticos

4. **Rate Limiting**
   ```python
   # Instalar
   pip install slowapi
   
   # En main.py
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

5. **SSL/TLS en Producción**
   - Certificados válidos (Let's Encrypt)
   - HSTS headers habilitados
   - Redirecciónnforzada de HTTP a HTTPS

---

## 🐛 Troubleshooting

### Error: "PostgreSQL connection refused"

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
connection refused
```

**Soluciones:**

```bash
# 1. Ver si PostgreSQL está corriendo
docker-compose ps db
# o
psql -U postgres  # Local

# 2. Verificar DATABASE_URL en .env
cat .env | grep DATABASE_URL

# 3. Conectar con psql
docker exec vm_postgres psql -U postgres -c "SELECT 1"

# 4. Ver logs de BD
docker-compose logs db
```

---

### Error: "Email already exists"

```
HTTPException: Email already exists
```

**Solución:**

```bash
# En BD
docker exec vm_postgres psql -U postgres observatorio_vm

# Delete user
DELETE FROM users WHERE email = 'admin@observatoriovm.org';

# O cambiar email en create_admin.py
```

---

### Error: "Invalid token"

```
HTTPException: No se pudieron validar las credenciales
```

**Soluciones:**

1. **Token expirado:** Login nuevamente
2. **JWT_SECRET_KEY cambió:** Tokens antiguos inválidos
3. **Token corrupto:** Limpiar localStorage en frontend

```bash
# Backend: Verificar JWT_SECRET_KEY
grep JWT_SECRET_KEY .env

# Frontend: Limpiar token
localStorage.clear()
```

---

### Error: "Alembic migration failed"

```
sqlalchemy.exc.IntegrityError: ...
```

**Soluciones:**

```bash
# Ver estado actual
alembic current

# Skip última si fue mal
alembic downgrade -1

# Ver todos los cambios
alembic history

# Revertir todo y restart
alembic downgrade base
alembic upgrade head
```

---

### Scraper no encuentra artículos

```bash
# 1. Verificar que spiders están definidos
python launcher.py --help

# 2. Ejecutar spider específico con debug
scrapy crawl eltiempo -a loglevel=DEBUG

# 3. Vaciar Redis y reintentar
python launcher.py --flush-redis

# 4. Ver logs
docker-compose logs -f scraper
```

---

## 📚 Recursos Útiles

### Documentación del Proyecto

- **[SECURITY_AUDIT_REPORT.md](./SECURITY_AUDIT_REPORT.md)**
  Auditoría de seguridad completa con vulnerabilidades halladas

- **[SECURITY_FIXES.md](./SECURITY_FIXES.md)**
  Soluciones técnicas implementadas

- **[.env.example](./.env.example)**
  Template de variables de entorno documentado

### Documentación Externa

- **[FastAPI Docs](https://fastapi.tiangolo.com)** - Framework web
- **[SQLAlchemy Docs](https://docs.sqlalchemy.org)** - ORM
- **[Alembic Docs](https://alembic.sqlalchemy.org)** - Migraciones
- **[Pydantic Docs](https://docs.pydantic.dev)** - Validación de datos
- **[Scrapy Docs](https://docs.scrapy.org)** - Web scraping
- **[PostgreSQL Docs](https://www.postgresql.org/docs)** - Base de datos
- **[OAuth2 Spec](https://oauth.net/2)** - Estándar de autenticación

---

## 🤝 Contribuciones

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crear rama** para feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commits descriptivos** siguiendo convención
4. **Push** a tu fork
5. **Pull Request** con descripción clara

### Estándares de Código

- ✅ Type hints en todas las funciones
- ✅ Docstrings con ejemplos
- ✅ PEP 8 compliance
- ✅ pytest para tests
- ✅ Manejo de excepciones apropiado

**Ejemplo de función bien documentada:**

```python
from typing import Optional
from sqlalchemy.orm import Session
from app.database.models import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user from the database by email.
    
    Args:
        db (Session): Database session
        email (str): User email to search for
    
    Returns:
        Optional[User]: User object if found, None otherwise
    
    Raises:
        ValueError: If email format is invalid
    
    Example:
        >>> user = get_user_by_email(db, "admin@example.com")
        >>> user.username
        'admin'
    """
    if not "@" in email:
        raise ValueError("Email format invalid")
    
    return db.query(User).filter(User.email == email).first()
```

---

## 📞 Soporte

- **📧 Email:** tecnologia@observatoriovm.org
- **🐛 Issues:** Reporta en GitHub
- **💬 Discussions:** Para preguntas
- **📖 Docs:** Lee documentación completa

---

## 📝 Licencia

Desarrollado por el equipo de Observatorio V&M.  
Confidencial - Uso interno únicamente.

---

**Última actualización:** 27 de marzo de 2026  
**Versión Actual:** 1.0.0  
**Status:** 🚀 En Desarrollo Activo  
**Mantenedor:** Equipo de Observatorio V&M


