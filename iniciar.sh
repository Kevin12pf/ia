#!/bin/bash

# Script para iniciar la aplicación en Linux/Mac

echo ""
echo "========================================"
echo "  Poniendome Riquisimo - Inicio Rápido"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Instala Python desde: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/3] Instalando dependencias del backend..."
cd backend
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
cd ..

echo "[2/3] Iniciando servidor backend (FastAPI)..."
echo ""
echo "El servidor estará disponible en: http://localhost:8000"
echo "Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar backend en background
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "[3/3] Abriendo frontend en navegador..."
echo ""
echo "El frontend estará disponible en: http://localhost:8080"
echo ""

# Intentar abrir el navegador
if command -v open &> /dev/null; then
    open http://localhost:8080
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
fi

# Iniciar servidor de frontend
cd frontend
python3 -m http.server 8080

# Limpiar al salir
trap "kill $BACKEND_PID" EXIT
