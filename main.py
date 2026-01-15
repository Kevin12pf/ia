from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
from PIL import Image
import io
import json
from datetime import datetime
import uvicorn

app = FastAPI(title="Poniendome Riquisimo API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELOS ====================

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre: str
    edad: int
    objetivo: str  # "recomposicion_corporal", "volumen", "definicion"
    email: Optional[str] = None
    password: Optional[str] = None

class MedidasPredichas(BaseModel):
    altura: float
    peso: float
    imc: float
    porcentaje_grasa: Optional[float] = None

class PlanNutricion(BaseModel):
    usuario_id: int
    calorias_diarias: float
    proteina_g: float
    carbohidratos_g: float
    grasas_g: float
    comidas: List[dict]
    alimentos_disponibles: List[str]

class PlanEjercicios(BaseModel):
    usuario_id: int
    objetivo: str
    dias_semana: List[dict]
    intensidad: str

class ResultadoDia(BaseModel):
    fecha: str
    usuario_id: int
    medidas: MedidasPredichas
    plan_nutricion: PlanNutricion
    plan_ejercicios: PlanEjercicios

# ==================== SIMULACIÓN DE MODELO CNN ====================

def predecir_medidas_cnn(imagen_frontal: Image.Image, imagen_lateral: Image.Image) -> MedidasPredichas:
    """
    Simula predicción del modelo CNN.
    En producción, aquí iría el modelo real entrenado.
    """
    # Simulación: valores basados en tamaño de imagen
    altura_estimada = 1.70 + np.random.uniform(-0.15, 0.15)
    peso_estimado = 75 + np.random.uniform(-20, 20)
    imc = peso_estimado / (altura_estimada ** 2)
    porcentaje_grasa = 20 + np.random.uniform(-10, 10)
    
    return MedidasPredichas(
        altura=round(altura_estimada, 2),
        peso=round(peso_estimado, 2),
        imc=round(imc, 2),
        porcentaje_grasa=round(porcentaje_grasa, 2)
    )

# ==================== GENERACIÓN DE PLANES ====================

def generar_plan_nutricion(usuario: Usuario, medidas: MedidasPredichas, alimentos: List[str]) -> PlanNutricion:
    """
    Genera plan de nutrición personalizado según objetivo.
    """
    # Cálculo de calorías basado en Harris-Benedict
    if usuario.objetivo == "volumen":
        multiplicador = 1.4
    elif usuario.objetivo == "definicion":
        multiplicador = 0.8
    else:  # recomposicion_corporal
        multiplicador = 1.1
    
    calorias_base = 1500 + (medidas.peso * 10)
    calorias_diarias = calorias_base * multiplicador
    
    # Macronutrientes según objetivo
    if usuario.objetivo == "volumen":
        proteina_g = medidas.peso * 2.2
        carbohidratos_g = medidas.peso * 4
        grasas_g = medidas.peso * 0.8
    elif usuario.objetivo == "definicion":
        proteina_g = medidas.peso * 2.5
        carbohidratos_g = medidas.peso * 2
        grasas_g = medidas.peso * 0.6
    else:  # recomposicion
        proteina_g = medidas.peso * 2.0
        carbohidratos_g = medidas.peso * 3
        grasas_g = medidas.peso * 0.7
    
    # Generar comidas del día
    comidas = [
        {
            "nombre": "Desayuno",
            "hora": "07:00",
            "calorias": calorias_diarias * 0.25,
            "alimentos": alimentos[:2] if len(alimentos) >= 2 else alimentos
        },
        {
            "nombre": "Almuerzo",
            "hora": "12:30",
            "calorias": calorias_diarias * 0.35,
            "alimentos": alimentos[2:4] if len(alimentos) >= 4 else alimentos[1:3]
        },
        {
            "nombre": "Merienda",
            "hora": "16:00",
            "calorias": calorias_diarias * 0.15,
            "alimentos": alimentos[4:5] if len(alimentos) >= 5 else [alimentos[-1]]
        },
        {
            "nombre": "Cena",
            "hora": "19:30",
            "calorias": calorias_diarias * 0.25,
            "alimentos": alimentos[5:7] if len(alimentos) >= 7 else alimentos[-2:]
        }
    ]
    
    return PlanNutricion(
        usuario_id=usuario.id or 1,
        calorias_diarias=round(calorias_diarias, 2),
        proteina_g=round(proteina_g, 2),
        carbohidratos_g=round(carbohidratos_g, 2),
        grasas_g=round(grasas_g, 2),
        comidas=comidas,
        alimentos_disponibles=alimentos
    )

def generar_plan_ejercicios(usuario: Usuario, medidas: MedidasPredichas) -> PlanEjercicios:
    """
    Genera plan de ejercicios personalizado según objetivo.
    """
    if usuario.objetivo == "volumen":
        intensidad = "Alta"
        dias = [
            {
                "dia": "Lunes",
                "grupo_muscular": "Pecho y Tríceps",
                "ejercicios": [
                    {"nombre": "Press de Banca", "series": 4, "repeticiones": 8, "descanso": 90},
                    {"nombre": "Aperturas con Mancuernas", "series": 3, "repeticiones": 10, "descanso": 60},
                    {"nombre": "Fondos", "series": 3, "repeticiones": 8, "descanso": 60}
                ]
            },
            {
                "dia": "Martes",
                "grupo_muscular": "Espalda y Bíceps",
                "ejercicios": [
                    {"nombre": "Dominadas", "series": 4, "repeticiones": 8, "descanso": 90},
                    {"nombre": "Remo con Barra", "series": 4, "repeticiones": 8, "descanso": 90},
                    {"nombre": "Curl de Bíceps", "series": 3, "repeticiones": 10, "descanso": 60}
                ]
            },
            {
                "dia": "Miércoles",
                "grupo_muscular": "Descanso o Cardio Ligero",
                "ejercicios": [
                    {"nombre": "Caminata", "series": 1, "repeticiones": 30, "descanso": 0}
                ]
            },
            {
                "dia": "Jueves",
                "grupo_muscular": "Piernas",
                "ejercicios": [
                    {"nombre": "Sentadillas", "series": 4, "repeticiones": 8, "descanso": 90},
                    {"nombre": "Prensa de Piernas", "series": 3, "repeticiones": 10, "descanso": 60},
                    {"nombre": "Extensiones de Cuádriceps", "series": 3, "repeticiones": 12, "descanso": 45}
                ]
            },
            {
                "dia": "Viernes",
                "grupo_muscular": "Hombros",
                "ejercicios": [
                    {"nombre": "Press Militar", "series": 4, "repeticiones": 8, "descanso": 90},
                    {"nombre": "Elevaciones Laterales", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Pájaros", "series": 3, "repeticiones": 12, "descanso": 60}
                ]
            },
            {
                "dia": "Sábado",
                "grupo_muscular": "Brazos y Abdominales",
                "ejercicios": [
                    {"nombre": "Curl de Bíceps", "series": 3, "repeticiones": 12, "descanso": 45},
                    {"nombre": "Extensiones de Tríceps", "series": 3, "repeticiones": 12, "descanso": 45},
                    {"nombre": "Abdominales", "series": 3, "repeticiones": 20, "descanso": 30}
                ]
            },
            {
                "dia": "Domingo",
                "grupo_muscular": "Descanso",
                "ejercicios": []
            }
        ]
    elif usuario.objetivo == "definicion":
        intensidad = "Media-Alta"
        dias = [
            {
                "dia": "Lunes",
                "grupo_muscular": "Cardio + Pecho",
                "ejercicios": [
                    {"nombre": "Cardio (Trote)", "series": 1, "repeticiones": 20, "descanso": 0},
                    {"nombre": "Press de Banca", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Aperturas", "series": 3, "repeticiones": 15, "descanso": 45}
                ]
            },
            {
                "dia": "Martes",
                "grupo_muscular": "Espalda",
                "ejercicios": [
                    {"nombre": "Remo", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Jalones", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Remo Invertido", "series": 3, "repeticiones": 15, "descanso": 45}
                ]
            },
            {
                "dia": "Miércoles",
                "grupo_muscular": "Cardio Intenso",
                "ejercicios": [
                    {"nombre": "HIIT", "series": 1, "repeticiones": 30, "descanso": 0}
                ]
            },
            {
                "dia": "Jueves",
                "grupo_muscular": "Piernas",
                "ejercicios": [
                    {"nombre": "Sentadillas", "series": 3, "repeticiones": 15, "descanso": 60},
                    {"nombre": "Estocadas", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Pantorrillas", "series": 3, "repeticiones": 20, "descanso": 45}
                ]
            },
            {
                "dia": "Viernes",
                "grupo_muscular": "Brazos y Hombros",
                "ejercicios": [
                    {"nombre": "Curl de Bíceps", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Extensiones de Tríceps", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Press Militar", "series": 3, "repeticiones": 12, "descanso": 60}
                ]
            },
            {
                "dia": "Sábado",
                "grupo_muscular": "Cardio Moderado",
                "ejercicios": [
                    {"nombre": "Caminata Rápida", "series": 1, "repeticiones": 45, "descanso": 0}
                ]
            },
            {
                "dia": "Domingo",
                "grupo_muscular": "Descanso",
                "ejercicios": []
            }
        ]
    else:  # recomposicion_corporal
        intensidad = "Media"
        dias = [
            {
                "dia": "Lunes",
                "grupo_muscular": "Pecho y Tríceps",
                "ejercicios": [
                    {"nombre": "Press de Banca", "series": 3, "repeticiones": 10, "descanso": 75},
                    {"nombre": "Aperturas", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Fondos", "series": 3, "repeticiones": 10, "descanso": 60}
                ]
            },
            {
                "dia": "Martes",
                "grupo_muscular": "Cardio Ligero",
                "ejercicios": [
                    {"nombre": "Caminata", "series": 1, "repeticiones": 30, "descanso": 0}
                ]
            },
            {
                "dia": "Miércoles",
                "grupo_muscular": "Espalda y Bíceps",
                "ejercicios": [
                    {"nombre": "Remo", "series": 3, "repeticiones": 10, "descanso": 75},
                    {"nombre": "Jalones", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Curl de Bíceps", "series": 3, "repeticiones": 12, "descanso": 60}
                ]
            },
            {
                "dia": "Jueves",
                "grupo_muscular": "Descanso",
                "ejercicios": []
            },
            {
                "dia": "Viernes",
                "grupo_muscular": "Piernas",
                "ejercicios": [
                    {"nombre": "Sentadillas", "series": 3, "repeticiones": 10, "descanso": 75},
                    {"nombre": "Prensa", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Extensiones", "series": 3, "repeticiones": 12, "descanso": 60}
                ]
            },
            {
                "dia": "Sábado",
                "grupo_muscular": "Hombros y Abdominales",
                "ejercicios": [
                    {"nombre": "Press Militar", "series": 3, "repeticiones": 10, "descanso": 75},
                    {"nombre": "Elevaciones Laterales", "series": 3, "repeticiones": 12, "descanso": 60},
                    {"nombre": "Abdominales", "series": 3, "repeticiones": 15, "descanso": 45}
                ]
            },
            {
                "dia": "Domingo",
                "grupo_muscular": "Descanso",
                "ejercicios": []
            }
        ]
    
    return PlanEjercicios(
        usuario_id=usuario.id or 1,
        objetivo=usuario.objetivo,
        dias_semana=dias,
        intensidad=intensidad
    )

# ==================== ENDPOINTS ====================

@app.post("/api/auth/register")
async def registrar_usuario(usuario: Usuario):
    """Registra un nuevo usuario"""
    try:
        # Aquí iría la lógica de base de datos
        usuario.id = 1  # Simulado
        return {
            "success": True,
            "message": "Usuario registrado exitosamente",
            "usuario": usuario
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
async def login_usuario(email: str, password: str):
    """Login de usuario"""
    try:
        # Aquí iría la lógica de base de datos
        return {
            "success": True,
            "message": "Login exitoso",
            "token": "token_simulado_123",
            "usuario_id": 1
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.post("/api/medidas/predecir")
async def predecir_medidas(
    imagen_frontal: UploadFile = File(...),
    imagen_lateral: UploadFile = File(...),
    usuario_id: int = 1
):
    """
    Predice medidas usando el modelo CNN.
    Recibe dos imágenes (frontal y lateral) y retorna altura, peso, IMC, etc.
    """
    try:
        # Leer imágenes
        frontal_data = await imagen_frontal.read()
        lateral_data = await imagen_lateral.read()
        
        img_frontal = Image.open(io.BytesIO(frontal_data))
        img_lateral = Image.open(io.BytesIO(lateral_data))
        
        # Predecir medidas
        medidas = predecir_medidas_cnn(img_frontal, img_lateral)
        
        return {
            "success": True,
            "medidas": medidas,
            "usuario_id": usuario_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar imágenes: {str(e)}")

@app.post("/api/planes/generar")
async def generar_planes(
    usuario: Usuario,
    medidas: MedidasPredichas,
    alimentos_disponibles: List[str]
):
    """
    Genera planes de nutrición y ejercicios personalizados.
    """
    try:
        plan_nutricion = generar_plan_nutricion(usuario, medidas, alimentos_disponibles)
        plan_ejercicios = generar_plan_ejercicios(usuario, medidas)
        
        resultado = ResultadoDia(
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            usuario_id=usuario.id or 1,
            medidas=medidas,
            plan_nutricion=plan_nutricion,
            plan_ejercicios=plan_ejercicios
        )
        
        return {
            "success": True,
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/usuario/{usuario_id}")
async def obtener_usuario(usuario_id: int):
    """Obtiene información del usuario"""
    try:
        # Aquí iría la lógica de base de datos
        return {
            "success": True,
            "usuario": {
                "id": usuario_id,
                "nombre": "Juan Pérez",
                "edad": 28,
                "objetivo": "volumen",
                "email": "juan@example.com"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/api/planes/{usuario_id}")
async def obtener_planes(usuario_id: int):
    """Obtiene los planes del usuario"""
    try:
        # Aquí iría la lógica de base de datos
        return {
            "success": True,
            "planes": []
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Planes no encontrados")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a Poniendome Riquisimo API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
