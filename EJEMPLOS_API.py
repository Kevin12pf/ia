"""
Ejemplos de uso de la API - Poniendome Riquisimo

Este archivo contiene ejemplos de cómo usar los endpoints de la API
desde Python, JavaScript y cURL.
"""

# ==================== PYTHON ====================

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api"

# 1. REGISTRAR USUARIO
def registrar_usuario():
    """Registra un nuevo usuario"""
    url = f"{BASE_URL}/auth/register"
    
    datos = {
        "nombre": "Juan Pérez",
        "edad": 28,
        "email": "juan@example.com",
        "password": "123456",
        "objetivo": "volumen"
    }
    
    response = requests.post(url, json=datos)
    print(response.json())
    return response.json()

# 2. LOGIN
def login_usuario():
    """Inicia sesión"""
    url = f"{BASE_URL}/auth/login"
    
    params = {
        "email": "juan@example.com",
        "password": "123456"
    }
    
    response = requests.post(url, params=params)
    print(response.json())
    return response.json()

# 3. PREDECIR MEDIDAS
def predecir_medidas():
    """Predice medidas a partir de fotos"""
    url = f"{BASE_URL}/medidas/predecir"
    
    # Cargar imágenes
    with open("foto_frontal.jpg", "rb") as f_frontal:
        with open("foto_lateral.jpg", "rb") as f_lateral:
            files = {
                "imagen_frontal": f_frontal,
                "imagen_lateral": f_lateral
            }
            
            params = {"usuario_id": 1}
            
            response = requests.post(url, files=files, params=params)
            print(response.json())
            return response.json()

# 4. GENERAR PLANES
def generar_planes():
    """Genera planes personalizados"""
    url = f"{BASE_URL}/planes/generar"
    
    datos = {
        "usuario": {
            "id": 1,
            "nombre": "Juan Pérez",
            "edad": 28,
            "objetivo": "volumen",
            "email": "juan@example.com"
        },
        "medidas": {
            "altura": 1.75,
            "peso": 80.5,
            "imc": 26.2,
            "porcentaje_grasa": 22.5
        },
        "alimentos_disponibles": [
            "Pollo",
            "Arroz",
            "Brócoli",
            "Huevos",
            "Avena",
            "Salmón",
            "Plátano"
        ]
    }
    
    response = requests.post(url, json=datos)
    resultado = response.json()
    
    # Guardar resultado
    with open("resultado_planes.json", "w") as f:
        json.dump(resultado, f, indent=2)
    
    print(resultado)
    return resultado

# 5. OBTENER USUARIO
def obtener_usuario(usuario_id: int):
    """Obtiene información del usuario"""
    url = f"{BASE_URL}/usuario/{usuario_id}"
    
    response = requests.get(url)
    print(response.json())
    return response.json()

# 6. OBTENER PLANES
def obtener_planes(usuario_id: int):
    """Obtiene los planes del usuario"""
    url = f"{BASE_URL}/planes/{usuario_id}"
    
    response = requests.get(url)
    print(response.json())
    return response.json()

# Ejecutar ejemplos
if __name__ == "__main__":
    print("=== Ejemplos de API ===\n")
    
    # Registrar
    print("1. Registrando usuario...")
    registrar_usuario()
    
    # Login
    print("\n2. Iniciando sesión...")
    login_usuario()
    
    # Obtener usuario
    print("\n3. Obteniendo información del usuario...")
    obtener_usuario(1)
    
    # Obtener planes
    print("\n4. Obteniendo planes...")
    obtener_planes(1)


# ==================== JAVASCRIPT ====================

"""
// 1. REGISTRAR USUARIO
async function registrarUsuario() {
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: 'Juan Pérez',
            edad: 28,
            email: 'juan@example.com',
            password: '123456',
            objetivo: 'volumen'
        })
    });
    
    const data = await response.json();
    console.log(data);
    return data;
}

// 2. LOGIN
async function loginUsuario() {
    const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: 'juan@example.com',
            password: '123456'
        })
    });
    
    const data = await response.json();
    console.log(data);
    return data;
}

// 3. PREDECIR MEDIDAS
async function predecirMedidas(fotoFrontal, fotoLateral) {
    const formData = new FormData();
    formData.append('imagen_frontal', fotoFrontal);
    formData.append('imagen_lateral', fotoLateral);
    formData.append('usuario_id', 1);
    
    const response = await fetch('http://localhost:8000/api/medidas/predecir', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    console.log(data);
    return data;
}

// 4. GENERAR PLANES
async function generarPlanes() {
    const response = await fetch('http://localhost:8000/api/planes/generar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            usuario: {
                id: 1,
                nombre: 'Juan Pérez',
                edad: 28,
                objetivo: 'volumen',
                email: 'juan@example.com'
            },
            medidas: {
                altura: 1.75,
                peso: 80.5,
                imc: 26.2,
                porcentaje_grasa: 22.5
            },
            alimentos_disponibles: [
                'Pollo', 'Arroz', 'Brócoli', 'Huevos',
                'Avena', 'Salmón', 'Plátano'
            ]
        })
    });
    
    const data = await response.json();
    console.log(data);
    return data;
}

// 5. OBTENER USUARIO
async function obtenerUsuario(usuarioId) {
    const response = await fetch(`http://localhost:8000/api/usuario/${usuarioId}`);
    const data = await response.json();
    console.log(data);
    return data;
}

// 6. OBTENER PLANES
async function obtenerPlanes(usuarioId) {
    const response = await fetch(`http://localhost:8000/api/planes/${usuarioId}`);
    const data = await response.json();
    console.log(data);
    return data;
}

// Ejecutar ejemplos
async function ejecutarEjemplos() {
    console.log('=== Ejemplos de API ===\n');
    
    console.log('1. Registrando usuario...');
    await registrarUsuario();
    
    console.log('\n2. Iniciando sesión...');
    await loginUsuario();
    
    console.log('\n3. Obteniendo usuario...');
    await obtenerUsuario(1);
    
    console.log('\n4. Obteniendo planes...');
    await obtenerPlanes(1);
}

// Ejecutar
ejecutarEjemplos();
"""


# ==================== CURL ====================

"""
# 1. REGISTRAR USUARIO
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "edad": 28,
    "email": "juan@example.com",
    "password": "123456",
    "objetivo": "volumen"
  }'

# 2. LOGIN
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "123456"
  }'

# 3. PREDECIR MEDIDAS
curl -X POST "http://localhost:8000/api/medidas/predecir" \
  -F "imagen_frontal=@foto_frontal.jpg" \
  -F "imagen_lateral=@foto_lateral.jpg" \
  -F "usuario_id=1"

# 4. GENERAR PLANES
curl -X POST "http://localhost:8000/api/planes/generar" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": {
      "id": 1,
      "nombre": "Juan Pérez",
      "edad": 28,
      "objetivo": "volumen",
      "email": "juan@example.com"
    },
    "medidas": {
      "altura": 1.75,
      "peso": 80.5,
      "imc": 26.2,
      "porcentaje_grasa": 22.5
    },
    "alimentos_disponibles": [
      "Pollo", "Arroz", "Brócoli", "Huevos",
      "Avena", "Salmón", "Plátano"
    ]
  }'

# 5. OBTENER USUARIO
curl -X GET "http://localhost:8000/api/usuario/1"

# 6. OBTENER PLANES
curl -X GET "http://localhost:8000/api/planes/1"

# 7. VER DOCUMENTACIÓN
curl -X GET "http://localhost:8000/docs"
"""


# ==================== POSTMAN ====================

"""
Importar en Postman:

1. Crear nueva colección: "Poniendome Riquisimo"

2. Crear requests:

   POST /api/auth/register
   Body (JSON):
   {
     "nombre": "Juan Pérez",
     "edad": 28,
     "email": "juan@example.com",
     "password": "123456",
     "objetivo": "volumen"
   }

   POST /api/auth/login
   Body (JSON):
   {
     "email": "juan@example.com",
     "password": "123456"
   }

   POST /api/medidas/predecir
   Body (form-data):
   - imagen_frontal: [archivo]
   - imagen_lateral: [archivo]
   - usuario_id: 1

   POST /api/planes/generar
   Body (JSON):
   {
     "usuario": {...},
     "medidas": {...},
     "alimentos_disponibles": [...]
   }

   GET /api/usuario/1

   GET /api/planes/1
"""


# ==================== RESPUESTAS ESPERADAS ====================

"""
1. REGISTRAR USUARIO
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "edad": 28,
    "objetivo": "volumen",
    "email": "juan@example.com"
  }
}

2. LOGIN
{
  "success": true,
  "message": "Login exitoso",
  "token": "token_simulado_123",
  "usuario_id": 1
}

3. PREDECIR MEDIDAS
{
  "success": true,
  "medidas": {
    "altura": 1.75,
    "peso": 80.5,
    "imc": 26.2,
    "porcentaje_grasa": 22.5
  },
  "usuario_id": 1
}

4. GENERAR PLANES
{
  "success": true,
  "resultado": {
    "fecha": "2026-01-14 18:47:21",
    "usuario_id": 1,
    "medidas": {...},
    "plan_nutricion": {...},
    "plan_ejercicios": {...}
  }
}

5. OBTENER USUARIO
{
  "success": true,
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "edad": 28,
    "objetivo": "volumen",
    "email": "juan@example.com"
  }
}

6. OBTENER PLANES
{
  "success": true,
  "planes": []
}
"""
