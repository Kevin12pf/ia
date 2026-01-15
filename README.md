# 💪 Poniendome Riquisimo

Aplicación web completa para nutrición y entrenamiento personalizado usando IA (CNN) para análisis de medidas corporales.

## 🎯 Características

- **Autenticación**: Registro e inicio de sesión de usuarios
- **Análisis de Medidas**: Carga de fotos (frontal y lateral) para predicción de altura, peso, IMC y porcentaje de grasa usando modelo CNN
- **Planes Personalizados**: Generación automática de planes de nutrición y ejercicios según objetivo
- **Objetivos Disponibles**:
  - Volumen (Ganar Masa Muscular)
  - Definición (Perder Grasa)
  - Recomposición Corporal
- **Interfaz Intuitiva**: Diseño moderno y responsivo

## 📁 Estructura del Proyecto

```
poniendome_riquisimo/
├── frontend/
│   ├── index.html          # Página principal
│   ├── styles.css          # Estilos
│   └── script.js           # Lógica del cliente
├── backend/
│   ├── main.py             # API FastAPI
│   └── requirements.txt     # Dependencias Python
└── README.md               # Este archivo
```

## 🚀 Instalación y Ejecución

### Backend (FastAPI)

1. **Instalar dependencias**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Ejecutar el servidor**:
```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

### Frontend

1. **Abrir en navegador**:
   - Simplemente abre el archivo `frontend/index.html` en tu navegador
   - O usa un servidor local (recomendado):

```bash
# Con Python 3
cd frontend
python -m http.server 8080

# O con Node.js
npx http-server
```

Accede a `http://localhost:8080`

## 📋 Flujo de Uso

1. **Registro/Login**: Crea una cuenta o inicia sesión
2. **Ingresa Datos Básicos**: Nombre, edad y objetivo
3. **Carga Fotos**: Sube foto frontal y lateral
4. **Análisis**: El modelo CNN predice tus medidas
5. **Alimentos**: Ingresa los alimentos disponibles
6. **Planes**: Recibe plan de nutrición y ejercicios personalizados

## 🔌 Endpoints API

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión

### Medidas
- `POST /api/medidas/predecir` - Predecir medidas con CNN

### Planes
- `POST /api/planes/generar` - Generar planes personalizados
- `GET /api/planes/{usuario_id}` - Obtener planes del usuario

### Usuario
- `GET /api/usuario/{usuario_id}` - Obtener información del usuario

## 🤖 Modelo CNN

Actualmente, el modelo CNN está simulado. Para integrar tu modelo real:

1. Reemplaza la función `predecir_medidas_cnn()` en `backend/main.py`
2. Carga tu modelo entrenado
3. Procesa las imágenes y retorna las predicciones

Ejemplo:
```python
def predecir_medidas_cnn(imagen_frontal: Image.Image, imagen_lateral: Image.Image) -> MedidasPredichas:
    # Cargar modelo
    modelo = load_model('tu_modelo.h5')
    
    # Procesar imágenes
    img_frontal_procesada = procesar_imagen(imagen_frontal)
    img_lateral_procesada = procesar_imagen(imagen_lateral)
    
    # Predecir
    predicciones = modelo.predict([img_frontal_procesada, img_lateral_procesada])
    
    return MedidasPredichas(
        altura=predicciones[0],
        peso=predicciones[1],
        imc=predicciones[2],
        porcentaje_grasa=predicciones[3]
    )
```

## 💾 Base de Datos

Actualmente, los datos se simulan en memoria. Para integrar una base de datos:

1. Instala SQLAlchemy: `pip install sqlalchemy`
2. Configura tu base de datos (PostgreSQL, MySQL, SQLite)
3. Crea modelos ORM
4. Reemplaza las funciones de simulación con consultas reales

## 🎨 Personalización

### Colores
Edita las variables CSS en `frontend/styles.css`:
```css
:root {
    --primary-color: #FF6B35;
    --secondary-color: #004E89;
    --accent-color: #F7931E;
    /* ... más colores */
}
```

### Planes de Ejercicios
Modifica la función `generar_plan_ejercicios()` en `backend/main.py` para cambiar los ejercicios según objetivo.

### Cálculos de Nutrición
Ajusta los multiplicadores y ratios en `generar_plan_nutricion()` según tus necesidades.

## 📱 Responsive Design

La aplicación es completamente responsiva y funciona en:
- Desktop
- Tablet
- Mobile

## 🔐 Seguridad (Próximas Mejoras)

- [ ] Implementar JWT para autenticación
- [ ] Hash de contraseñas con bcrypt
- [ ] Validación de entrada
- [ ] Rate limiting
- [ ] HTTPS

## 📊 Próximas Características

- [ ] Historial de medidas
- [ ] Seguimiento de progreso
- [ ] Gráficos de evolución
- [ ] Integración con wearables
- [ ] Notificaciones
- [ ] Exportar planes a PDF
- [ ] Comunidad y desafíos

## 🛠️ Tecnologías Utilizadas

### Frontend
- HTML5
- CSS3
- JavaScript Vanilla

### Backend
- FastAPI
- Python 3.8+
- Pillow (procesamiento de imágenes)
- NumPy

## 📝 Licencia

Este proyecto es de código abierto.

## 👨‍💻 Autor

Desarrollado con ❤️ para ayudarte a ponerte riquisimo

## 📞 Soporte

Para reportar bugs o sugerencias, crea un issue en el repositorio.

---

**¡Empezá tu transformación hoy! 💪**
