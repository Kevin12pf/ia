# 🚀 GUÍA RÁPIDA DE INICIO

## Requisitos Previos
- Python 3.8 o superior
- Navegador web moderno
- Git (opcional)

## Instalación Rápida (Windows)

### 1. Instalar Backend

```bash
# Navegar a la carpeta del backend
cd backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Backend

```bash
# Desde la carpeta backend
python main.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Abrir Frontend

```bash
# Opción 1: Abrir directamente en navegador
# Navega a: C:\Users\DELL\.qodo\poniendome_riquisimo\frontend\index.html

# Opción 2: Usar servidor local (recomendado)
cd frontend
python -m http.server 8080
```

Luego abre en tu navegador: `http://localhost:8080`

## Prueba Rápida

1. **Registrarse**:
   - Nombre: Juan Pérez
   - Edad: 28
   - Email: juan@example.com
   - Contraseña: 123456
   - Objetivo: Volumen

2. **Cargar Fotos**:
   - Usa cualquier imagen JPG/PNG
   - Carga una como "Foto Frontal"
   - Carga otra como "Foto Lateral"
   - Haz clic en "Analizar Fotos"

3. **Agregar Alimentos**:
   - Escribe: Pollo
   - Presiona Enter o haz clic en "Agregar"
   - Repite con: Arroz, Brócoli, Huevos, Avena, Salmón

4. **Generar Planes**:
   - Haz clic en "Generar Planes Personalizados"
   - Verás tu plan de nutrición y ejercicios

## Estructura de Carpetas

```
C:\Users\DELL\.qodo\poniendome_riquisimo\
├── frontend/
│   ├── index.html          ← Abre esto en el navegador
│   ├── styles.css
│   └── script.js
├── backend/
│   ├── main.py             ← Ejecuta esto con Python
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
├── README.md
├── QUICKSTART.md            ← Este archivo
└── package.json
```

## Solución de Problemas

### Error: "Port 8000 already in use"
```bash
# Cambiar puerto en main.py
# Línea final: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Error: "Module not found"
```bash
# Asegúrate de instalar las dependencias
pip install -r requirements.txt
```

### Frontend no se conecta al backend
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Abre la consola del navegador (F12) para ver errores
- Comprueba que CORS esté habilitado en main.py

### Las fotos no se procesan
- Usa imágenes en formato JPG o PNG
- Asegúrate de que el tamaño sea razonable (< 5MB)
- Verifica que ambas fotos estén cargadas

## Próximos Pasos

1. **Integrar Base de Datos**:
   - Descomenta el código en `backend/models.py`
   - Instala: `pip install sqlalchemy`
   - Configura tu base de datos

2. **Integrar Modelo CNN Real**:
   - Reemplaza `predecir_medidas_cnn()` en `main.py`
   - Carga tu modelo entrenado
   - Procesa las imágenes correctamente

3. **Mejorar Seguridad**:
   - Implementa JWT
   - Hash de contraseñas
   - Validación de entrada

4. **Desplegar**:
   - Backend: Heroku, Railway, AWS
   - Frontend: Vercel, Netlify, GitHub Pages

## Comandos Útiles

```bash
# Ver documentación de API
http://localhost:8000/docs

# Instalar paquete específico
pip install nombre_paquete

# Crear requirements.txt
pip freeze > requirements.txt

# Ejecutar con debug
python -m pdb main.py
```

## Contacto y Soporte

Si tienes problemas:
1. Revisa la consola del navegador (F12)
2. Revisa los logs del servidor
3. Verifica que todos los puertos estén disponibles
4. Intenta reiniciar el servidor

---

**¡Listo para empezar! 💪**

Cualquier duda, revisa el README.md para más información.
