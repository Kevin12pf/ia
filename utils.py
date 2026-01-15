"""
Utilidades para el backend
"""

import json
from datetime import datetime
from typing import List, Dict, Any

def generar_resultado_json(usuario_id: int, medidas: Dict, plan_nutricion: Dict, plan_ejercicios: Dict) -> Dict:
    """
    Genera un JSON con el resultado del día (similar al archivo resultado_deia_*.json)
    """
    resultado = {
        "fecha": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "usuario_id": usuario_id,
        "medidas": {
            "altura": medidas.get("altura"),
            "peso": medidas.get("peso"),
            "imc": medidas.get("imc"),
            "porcentaje_grasa": medidas.get("porcentaje_grasa")
        },
        "plan_nutricion": {
            "calorias_diarias": plan_nutricion.get("calorias_diarias"),
            "macronutrientes": {
                "proteina_g": plan_nutricion.get("proteina_g"),
                "carbohidratos_g": plan_nutricion.get("carbohidratos_g"),
                "grasas_g": plan_nutricion.get("grasas_g")
            },
            "comidas": plan_nutricion.get("comidas", []),
            "alimentos_disponibles": plan_nutricion.get("alimentos_disponibles", [])
        },
        "plan_ejercicios": {
            "objetivo": plan_ejercicios.get("objetivo"),
            "intensidad": plan_ejercicios.get("intensidad"),
            "dias_semana": plan_ejercicios.get("dias_semana", [])
        }
    }
    
    return resultado


def guardar_resultado_json(resultado: Dict, ruta: str = None) -> str:
    """
    Guarda el resultado en un archivo JSON
    """
    if ruta is None:
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"resultado_deia_{fecha}.json"
    
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    return ruta


def calcular_imc(peso: float, altura: float) -> float:
    """
    Calcula el Índice de Masa Corporal
    """
    return peso / (altura ** 2)


def clasificar_imc(imc: float) -> str:
    """
    Clasifica el IMC según estándares de la OMS
    """
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"


def calcular_calorias_harris_benedict(peso: float, altura: float, edad: int, sexo: str = "M") -> float:
    """
    Calcula el gasto calórico basal usando la fórmula de Harris-Benedict
    """
    if sexo.upper() == "M":
        return 88.362 + (13.397 * peso) + (4.799 * altura * 100) - (5.677 * edad)
    else:
        return 447.593 + (9.247 * peso) + (3.098 * altura * 100) - (4.330 * edad)


def calcular_macronutrientes(calorias: float, objetivo: str) -> Dict[str, float]:
    """
    Calcula la distribución de macronutrientes según el objetivo
    """
    if objetivo == "volumen":
        # 30% proteína, 50% carbohidratos, 20% grasas
        proteina_cal = calorias * 0.30
        carbohidratos_cal = calorias * 0.50
        grasas_cal = calorias * 0.20
    elif objetivo == "definicion":
        # 35% proteína, 40% carbohidratos, 25% grasas
        proteina_cal = calorias * 0.35
        carbohidratos_cal = calorias * 0.40
        grasas_cal = calorias * 0.25
    else:  # recomposicion_corporal
        # 30% proteína, 45% carbohidratos, 25% grasas
        proteina_cal = calorias * 0.30
        carbohidratos_cal = calorias * 0.45
        grasas_cal = calorias * 0.25
    
    return {
        "proteina_g": proteina_cal / 4,  # 4 calorías por gramo
        "carbohidratos_g": carbohidratos_cal / 4,
        "grasas_g": grasas_cal / 9  # 9 calorías por gramo
    }


def generar_comidas_del_dia(alimentos: List[str], calorias_diarias: float) -> List[Dict]:
    """
    Genera un plan de comidas del día
    """
    comidas = [
        {
            "nombre": "Desayuno",
            "hora": "07:00",
            "porcentaje_calorias": 0.25,
            "alimentos": alimentos[:2] if len(alimentos) >= 2 else alimentos
        },
        {
            "nombre": "Almuerzo",
            "hora": "12:30",
            "porcentaje_calorias": 0.35,
            "alimentos": alimentos[2:4] if len(alimentos) >= 4 else alimentos[1:3]
        },
        {
            "nombre": "Merienda",
            "hora": "16:00",
            "porcentaje_calorias": 0.15,
            "alimentos": alimentos[4:5] if len(alimentos) >= 5 else [alimentos[-1]]
        },
        {
            "nombre": "Cena",
            "hora": "19:30",
            "porcentaje_calorias": 0.25,
            "alimentos": alimentos[5:7] if len(alimentos) >= 7 else alimentos[-2:]
        }
    ]
    
    # Calcular calorías por comida
    for comida in comidas:
        comida["calorias"] = calorias_diarias * comida["porcentaje_calorias"]
        del comida["porcentaje_calorias"]
    
    return comidas


def validar_email(email: str) -> bool:
    """
    Valida el formato de un email
    """
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_edad(edad: int) -> bool:
    """
    Valida que la edad sea razonable
    """
    return 13 <= edad <= 120


def validar_objetivo(objetivo: str) -> bool:
    """
    Valida que el objetivo sea válido
    """
    objetivos_validos = ["volumen", "definicion", "recomposicion_corporal"]
    return objetivo in objetivos_validos


# Ejemplo de uso:
"""
from utils import generar_resultado_json, guardar_resultado_json

resultado = generar_resultado_json(
    usuario_id=1,
    medidas={"altura": 1.75, "peso": 80, "imc": 26.1, "porcentaje_grasa": 22},
    plan_nutricion={
        "calorias_diarias": 2500,
        "proteina_g": 200,
        "carbohidratos_g": 300,
        "grasas_g": 80,
        "comidas": [...],
        "alimentos_disponibles": [...]
    },
    plan_ejercicios={
        "objetivo": "volumen",
        "intensidad": "Alta",
        "dias_semana": [...]
    }
)

ruta = guardar_resultado_json(resultado)
print(f"Resultado guardado en: {ruta}")
"""
