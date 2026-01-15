@echo off
REM Script para iniciar la aplicación en Windows

echo.
echo ========================================
echo   Poniendome Riquisimo - Inicio Rápido
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias del backend...
cd backend
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
cd ..

echo [2/3] Iniciando servidor backend (FastAPI)...
echo.
echo El servidor estará disponible en: http://localhost:8000
echo Documentación API: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

start cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak

echo [3/3] Abriendo frontend en navegador...
echo.
echo El frontend estará disponible en: http://localhost:8080
echo.

REM Intentar abrir el navegador
start http://localhost:8080

REM Iniciar servidor de frontend
cd frontend
python -m http.server 8080

pause
