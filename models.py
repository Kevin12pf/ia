"""
Modelos de Base de Datos (SQLAlchemy)
Descomenta y usa cuando integres una base de datos real
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    objetivo = Column(String(50), nullable=False)  # volumen, definicion, recomposicion_corporal
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    medidas = relationship("Medidas", back_populates="usuario")
    planes_nutricion = relationship("PlanNutricion", back_populates="usuario")
    planes_ejercicios = relationship("PlanEjercicios", back_populates="usuario")
    
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)


class Medidas(Base):
    __tablename__ = "medidas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    porcentaje_grasa = Column(Float, nullable=True)
    fecha_medicion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="medidas")


class PlanNutricion(Base):
    __tablename__ = "planes_nutricion"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    calorias_diarias = Column(Float, nullable=False)
    proteina_g = Column(Float, nullable=False)
    carbohidratos_g = Column(Float, nullable=False)
    grasas_g = Column(Float, nullable=False)
    alimentos_disponibles = Column(Text, nullable=False)  # JSON string
    comidas = Column(Text, nullable=False)  # JSON string
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="planes_nutricion")


class PlanEjercicios(Base):
    __tablename__ = "planes_ejercicios"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    objetivo = Column(String(50), nullable=False)
    intensidad = Column(String(50), nullable=False)
    dias_semana = Column(Text, nullable=False)  # JSON string
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="planes_ejercicios")


class Alimento(Base):
    __tablename__ = "alimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    calorias_por_100g = Column(Float, nullable=False)
    proteina_g = Column(Float, nullable=False)
    carbohidratos_g = Column(Float, nullable=False)
    grasas_g = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)  # proteina, carbohidrato, grasa, etc


# Ejemplo de uso en main.py:
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./poniendome_riquisimo.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Usar en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/auth/register")
async def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Lógica con base de datos
    pass
"""
