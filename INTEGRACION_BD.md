# 💾 Guía de Integración de Base de Datos

## Descripción General

Este documento explica cómo integrar una base de datos real a la aplicación. Actualmente, los datos se simulan en memoria.

## Opciones de Base de Datos

### 1. SQLite (Desarrollo Local)
- **Ventaja**: Sin configuración, archivo local
- **Desventaja**: No es escalable
- **Ideal para**: Desarrollo y pruebas

### 2. PostgreSQL (Recomendado)
- **Ventaja**: Robusto, escalable, gratuito
- **Desventaja**: Requiere instalación
- **Ideal para**: Producción

### 3. MySQL
- **Ventaja**: Popular, fácil de usar
- **Desventaja**: Menos robusto que PostgreSQL
- **Ideal para**: Producción

## Instalación Rápida

### SQLite (Sin instalación)
```bash
# Ya viene con Python
pip install sqlalchemy
```

### PostgreSQL

**Windows**:
1. Descarga desde: https://www.postgresql.org/download/windows/
2. Instala con valores por defecto
3. Recuerda la contraseña del usuario `postgres`

**Linux**:
```bash
sudo apt-get install postgresql postgresql-contrib
```

**Mac**:
```bash
brew install postgresql
```

### MySQL

**Windows**:
1. Descarga desde: https://dev.mysql.com/downloads/mysql/
2. Instala con valores por defecto

**Linux**:
```bash
sudo apt-get install mysql-server
```

**Mac**:
```bash
brew install mysql
```

## Configuración

### 1. Instalar SQLAlchemy

```bash
pip install sqlalchemy
pip install psycopg2-binary  # Para PostgreSQL
pip install mysql-connector-python  # Para MySQL
```

### 2. Crear archivo `backend/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener URL de base de datos desde variables de entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./poniendome_riquisimo.db"
)

# Configuración específica por tipo de BD
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependencia para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Crea todas las tablas"""
    from models import Base
    Base.metadata.create_all(bind=engine)
```

### 3. Actualizar `backend/main.py`

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Usuario, Medidas, PlanNutricion, PlanEjercicios

# Crear tablas al iniciar
@app.on_event("startup")
async def startup():
    init_db()

# Endpoints con BD

@app.post("/api/auth/register")
async def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la BD"""
    # Verificar si el email ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        edad=usuario.edad,
        objetivo=usuario.objetivo
    )
    nuevo_usuario.set_password(usuario.password)
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "success": True,
        "message": "Usuario registrado exitosamente",
        "usuario": {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "email": nuevo_usuario.email
        }
    }

@app.post("/api/auth/login")
async def login_usuario(email: str, password: str, db: Session = Depends(get_db)):
    """Login de usuario"""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario or not usuario.verify_password(password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Aquí iría la generación de JWT
    return {
        "success": True,
        "message": "Login exitoso",
        "token": "token_jwt_aqui",
        "usuario_id": usuario.id
    }

@app.post("/api/medidas/predecir")
async def predecir_medidas(
    imagen_frontal: UploadFile = File(...),
    imagen_lateral: UploadFile = File(...),
    usuario_id: int = 1,
    db: Session = Depends(get_db)
):
    """Predice medidas y las guarda en BD"""
    try:
        # Procesar imágenes
        frontal_data = await imagen_frontal.read()
        lateral_data = await imagen_lateral.read()
        
        img_frontal = Image.open(io.BytesIO(frontal_data))
        img_lateral = Image.open(io.BytesIO(lateral_data))
        
        # Predecir medidas
        medidas = predecir_medidas_cnn(img_frontal, img_lateral)
        
        # Guardar en BD
        nueva_medida = Medidas(
            usuario_id=usuario_id,
            altura=medidas.altura,
            peso=medidas.peso,
            imc=medidas.imc,
            porcentaje_grasa=medidas.porcentaje_grasa
        )
        
        db.add(nueva_medida)
        db.commit()
        db.refresh(nueva_medida)
        
        return {
            "success": True,
            "medidas": medidas,
            "usuario_id": usuario_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/planes/generar")
async def generar_planes(
    usuario_id: int,
    medidas_id: int,
    alimentos_disponibles: List[str],
    db: Session = Depends(get_db)
):
    """Genera y guarda planes en BD"""
    try:
        # Obtener usuario y medidas
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        medidas = db.query(Medidas).filter(Medidas.id == medidas_id).first()
        
        if not usuario or not medidas:
            raise HTTPException(status_code=404, detail="Usuario o medidas no encontrados")
        
        # Generar planes
        plan_nutricion = generar_plan_nutricion(usuario, medidas, alimentos_disponibles)
        plan_ejercicios = generar_plan_ejercicios(usuario, medidas)
        
        # Guardar planes en BD
        nuevo_plan_nutricion = PlanNutricion(
            usuario_id=usuario_id,
            calorias_diarias=plan_nutricion.calorias_diarias,
            proteina_g=plan_nutricion.proteina_g,
            carbohidratos_g=plan_nutricion.carbohidratos_g,
            grasas_g=plan_nutricion.grasas_g,
            alimentos_disponibles=json.dumps(alimentos_disponibles),
            comidas=json.dumps(plan_nutricion.comidas)
        )
        
        nuevo_plan_ejercicios = PlanEjercicios(
            usuario_id=usuario_id,
            objetivo=usuario.objetivo,
            intensidad=plan_ejercicios.intensidad,
            dias_semana=json.dumps(plan_ejercicios.dias_semana)
        )
        
        db.add(nuevo_plan_nutricion)
        db.add(nuevo_plan_ejercicios)
        db.commit()
        
        return {
            "success": True,
            "plan_nutricion_id": nuevo_plan_nutricion.id,
            "plan_ejercicios_id": nuevo_plan_ejercicios.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/usuario/{usuario_id}")
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene información del usuario"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "objetivo": usuario.objetivo,
            "email": usuario.email,
            "fecha_registro": usuario.fecha_registro
        }
    }

@app.get("/api/medidas/{usuario_id}")
async def obtener_medidas(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene historial de medidas del usuario"""
    medidas = db.query(Medidas).filter(Medidas.usuario_id == usuario_id).all()
    
    return {
        "success": True,
        "medidas": [
            {
                "id": m.id,
                "altura": m.altura,
                "peso": m.peso,
                "imc": m.imc,
                "porcentaje_grasa": m.porcentaje_grasa,
                "fecha": m.fecha_medicion
            }
            for m in medidas
        ]
    }

@app.get("/api/planes/{usuario_id}")
async def obtener_planes(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene los planes del usuario"""
    planes_nutricion = db.query(PlanNutricion).filter(
        PlanNutricion.usuario_id == usuario_id
    ).all()
    
    planes_ejercicios = db.query(PlanEjercicios).filter(
        PlanEjercicios.usuario_id == usuario_id
    ).all()
    
    return {
        "success": True,
        "planes_nutricion": [
            {
                "id": p.id,
                "calorias_diarias": p.calorias_diarias,
                "fecha_creacion": p.fecha_creacion
            }
            for p in planes_nutricion
        ],
        "planes_ejercicios": [
            {
                "id": p.id,
                "objetivo": p.objetivo,
                "intensidad": p.intensidad,
                "fecha_creacion": p.fecha_creacion
            }
            for p in planes_ejercicios
        ]
    }
```

### 4. Actualizar `.env`

```
# SQLite (desarrollo)
DATABASE_URL=sqlite:///./poniendome_riquisimo.db

# PostgreSQL (producción)
# DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/poniendome_riquisimo

# MySQL (producción)
# DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/poniendome_riquisimo
```

## Migraciones (Alembic)

Para manejar cambios en el esquema:

```bash
pip install alembic

# Inicializar
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Crear tablas iniciales"

# Aplicar migración
alembic upgrade head
```

## Backup y Restauración

### PostgreSQL

```bash
# Backup
pg_dump -U postgres poniendome_riquisimo > backup.sql

# Restaurar
psql -U postgres poniendome_riquisimo < backup.sql
```

### MySQL

```bash
# Backup
mysqldump -u root -p poniendome_riquisimo > backup.sql

# Restaurar
mysql -u root -p poniendome_riquisimo < backup.sql
```

## Monitoreo

```python
# Agregar logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

## Rendimiento

```python
# Índices en modelos
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    fecha_registro = Column(DateTime, index=True)

# Caché
from functools import lru_cache

@lru_cache(maxsize=128)
def obtener_usuario_cache(usuario_id: int):
    # ...
    pass
```

## Seguridad

```python
# Validar entrada
from pydantic import validator

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    
    @validator('email')
    def email_valido(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v

# Encriptar contraseñas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

usuario.password_hash = pwd_context.hash(password)
```

---

**¡Base de datos integrada! 🎉**
