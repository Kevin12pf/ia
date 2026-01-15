# 🤖 Guía de Integración del Modelo CNN

## Descripción General

Este documento explica cómo integrar tu modelo CNN entrenado para predecir medidas corporales (altura, peso, IMC, porcentaje de grasa) a partir de dos imágenes (frontal y lateral).

## Estructura Actual

Actualmente, la función `predecir_medidas_cnn()` en `backend/main.py` está simulada:

```python
def predecir_medidas_cnn(imagen_frontal: Image.Image, imagen_lateral: Image.Image) -> MedidasPredichas:
    # Simulación: valores basados en tamaño de imagen
    altura_estimada = 1.70 + np.random.uniform(-0.15, 0.15)
    peso_estimado = 75 + np.random.uniform(-20, 20)
    imc = peso_estimado / (altura_estimada ** 2)
    porcentaje_grasa = 20 + np.random.uniform(-10, 10)
    
    return MedidasPredichas(...)
```

## Pasos para Integración

### 1. Preparar tu Modelo

Asegúrate de que tu modelo CNN esté guardado en un formato compatible:
- **TensorFlow/Keras**: `.h5` o `.pb`
- **PyTorch**: `.pt` o `.pth`
- **ONNX**: `.onnx`

Ejemplo de guardado:
```python
# TensorFlow/Keras
modelo.save('modelos/cnn_medidas.h5')

# PyTorch
torch.save(modelo.state_dict(), 'modelos/cnn_medidas.pt')
```

### 2. Crear Carpeta de Modelos

```bash
mkdir backend/modelos
# Copia tu modelo aquí
cp tu_modelo.h5 backend/modelos/cnn_medidas.h5
```

### 3. Instalar Dependencias Necesarias

Según tu framework:

```bash
# Para TensorFlow/Keras
pip install tensorflow

# Para PyTorch
pip install torch torchvision

# Para ONNX
pip install onnx onnxruntime
```

Actualiza `backend/requirements.txt`:
```
tensorflow==2.13.0
# o
torch==2.0.0
torchvision==0.15.0
```

### 4. Crear Módulo de Predicción

Crea un archivo `backend/cnn_predictor.py`:

```python
import numpy as np
from PIL import Image
import tensorflow as tf
from typing import Tuple

class CNNPredictor:
    def __init__(self, model_path: str):
        """Carga el modelo CNN"""
        self.modelo = tf.keras.models.load_model(model_path)
        self.input_size = (224, 224)  # Ajusta según tu modelo
    
    def preprocesar_imagen(self, imagen: Image.Image) -> np.ndarray:
        """
        Preprocesa la imagen para el modelo
        """
        # Redimensionar
        imagen_redimensionada = imagen.resize(self.input_size)
        
        # Convertir a array
        imagen_array = np.array(imagen_redimensionada)
        
        # Normalizar (ajusta según tu modelo)
        imagen_array = imagen_array / 255.0
        
        # Agregar dimensión de batch
        imagen_array = np.expand_dims(imagen_array, axis=0)
        
        return imagen_array
    
    def predecir(self, imagen_frontal: Image.Image, imagen_lateral: Image.Image) -> Tuple[float, float, float, float]:
        """
        Predice medidas a partir de dos imágenes
        
        Returns:
            (altura, peso, imc, porcentaje_grasa)
        """
        # Preprocesar imágenes
        frontal_procesada = self.preprocesar_imagen(imagen_frontal)
        lateral_procesada = self.preprocesar_imagen(imagen_lateral)
        
        # Concatenar imágenes (si tu modelo espera ambas)
        entrada = np.concatenate([frontal_procesada, lateral_procesada], axis=0)
        
        # Realizar predicción
        predicciones = self.modelo.predict(entrada)
        
        # Extraer valores (ajusta según tu modelo)
        altura = float(predicciones[0][0])
        peso = float(predicciones[0][1])
        porcentaje_grasa = float(predicciones[0][2])
        
        # Calcular IMC
        imc = peso / (altura ** 2)
        
        return altura, peso, imc, porcentaje_grasa
```

### 5. Actualizar main.py

Reemplaza la función `predecir_medidas_cnn()`:

```python
from cnn_predictor import CNNPredictor
import os

# Cargar modelo al iniciar
MODEL_PATH = os.getenv('MODEL_PATH', './modelos/cnn_medidas.h5')
predictor = CNNPredictor(MODEL_PATH)

def predecir_medidas_cnn(imagen_frontal: Image.Image, imagen_lateral: Image.Image) -> MedidasPredichas:
    """
    Predice medidas usando el modelo CNN real
    """
    try:
        altura, peso, imc, porcentaje_grasa = predictor.predecir(imagen_frontal, imagen_lateral)
        
        return MedidasPredichas(
            altura=round(altura, 2),
            peso=round(peso, 2),
            imc=round(imc, 2),
            porcentaje_grasa=round(porcentaje_grasa, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción CNN: {str(e)}")
```

### 6. Configurar Variables de Entorno

Crea o actualiza `.env`:

```
MODEL_PATH=./modelos/cnn_medidas.h5
MODEL_WEIGHTS_PATH=./modelos/cnn_medidas_weights.h5
```

En `main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH', './modelos/cnn_medidas.h5')
```

## Consideraciones Importantes

### Preprocesamiento de Imágenes

Tu modelo probablemente requiere:
- **Tamaño específico**: (224, 224), (256, 256), (512, 512), etc.
- **Normalización**: [0, 1] o [-1, 1]
- **Formato de color**: RGB, BGR, Escala de grises
- **Aumentación de datos**: Rotación, zoom, etc.

Ejemplo:
```python
def preprocesar_imagen(self, imagen: Image.Image) -> np.ndarray:
    # Convertir a RGB si es necesario
    if imagen.mode != 'RGB':
        imagen = imagen.convert('RGB')
    
    # Redimensionar
    imagen = imagen.resize((224, 224))
    
    # Convertir a array
    imagen_array = np.array(imagen, dtype=np.float32)
    
    # Normalizar según ImageNet
    imagen_array = imagen_array / 255.0
    media = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    imagen_array = (imagen_array - media) / std
    
    # Agregar batch
    imagen_array = np.expand_dims(imagen_array, axis=0)
    
    return imagen_array
```

### Validación de Entrada

Valida que las predicciones sean razonables:

```python
def validar_predicciones(altura: float, peso: float, porcentaje_grasa: float) -> bool:
    """Valida que las predicciones sean realistas"""
    # Altura: 1.40m a 2.20m
    if not (1.40 <= altura <= 2.20):
        return False
    
    # Peso: 30kg a 200kg
    if not (30 <= peso <= 200):
        return False
    
    # Porcentaje de grasa: 5% a 50%
    if not (5 <= porcentaje_grasa <= 50):
        return False
    
    return True
```

### Manejo de Errores

```python
try:
    altura, peso, imc, porcentaje_grasa = predictor.predecir(frontal, lateral)
    
    if not validar_predicciones(altura, peso, porcentaje_grasa):
        raise ValueError("Predicciones fuera de rango")
    
    return MedidasPredichas(...)
    
except tf.errors.InvalidArgumentError as e:
    raise HTTPException(status_code=400, detail="Formato de imagen inválido")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")
```

## Optimización

### Caché de Modelo

```python
class CNNPredictor:
    _instance = None
    
    def __new__(cls, model_path: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.modelo = tf.keras.models.load_model(model_path)
        return cls._instance
```

### Predicción por Lotes

```python
def predecir_lote(self, imagenes_frontal: List[Image.Image], 
                  imagenes_lateral: List[Image.Image]) -> List[Tuple]:
    """Predice múltiples imágenes a la vez"""
    frontal_procesada = np.vstack([self.preprocesar_imagen(img) for img in imagenes_frontal])
    lateral_procesada = np.vstack([self.preprocesar_imagen(img) for img in imagenes_lateral])
    
    predicciones = self.modelo.predict(np.concatenate([frontal_procesada, lateral_procesada]))
    
    return predicciones
```

### GPU

```python
import tensorflow as tf

# Verificar GPU disponible
print(tf.config.list_physical_devices('GPU'))

# Usar GPU específica
with tf.device('/GPU:0'):
    predicciones = self.modelo.predict(entrada)
```

## Testing

```python
# test_cnn.py
import unittest
from PIL import Image
import numpy as np

class TestCNNPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = CNNPredictor('./modelos/cnn_medidas.h5')
    
    def test_prediccion_valida(self):
        # Crear imagen de prueba
        img = Image.new('RGB', (224, 224), color='red')
        
        altura, peso, imc, grasa = self.predictor.predecir(img, img)
        
        self.assertGreater(altura, 1.4)
        self.assertLess(altura, 2.2)
        self.assertGreater(peso, 30)
        self.assertLess(peso, 200)

if __name__ == '__main__':
    unittest.main()
```

## Recursos Útiles

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [PyTorch Documentation](https://pytorch.org/)
- [OpenCV Image Processing](https://opencv.org/)
- [Scikit-image](https://scikit-image.org/)

## Soporte

Si tienes problemas con la integración:
1. Verifica que el modelo se carga correctamente
2. Prueba con imágenes de prueba
3. Revisa los logs de error
4. Valida el formato de entrada/salida

---

**¡Listo para integrar tu modelo CNN! 🚀**
