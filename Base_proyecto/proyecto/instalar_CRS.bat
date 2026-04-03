@echo off
chcp 65001 >nul
title Instalador CRS v2.0

echo ============================================
echo   CHRONOS REGISTRY SYSTEM — Instalador
echo   SENA CIDM · Ficha 3232672
echo ============================================
echo.

:: Verificar que Python esté instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" al instalar.
    pause
    exit /b 1
)

echo [OK] Python detectado:
python --version
echo.

:: Actualizar pip primero
echo [1/3] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo     pip actualizado.
echo.

:: Instalar bcrypt con wheel precompilado (evita error de compilador en Windows)
echo [2/3] Instalando bcrypt (precompilado para Windows)...
python -m pip install bcrypt --only-binary :all: --quiet
if %errorlevel% neq 0 (
    echo     Reintentando instalacion de bcrypt...
    python -m pip install bcrypt --quiet
)
echo     bcrypt instalado.
echo.

:: Instalar el resto de dependencias
echo [3/3] Instalando dependencias del proyecto...
python -m pip install ^
    mysql-connector-python ^
    pandas ^
    tkcalendar ^
    openpyxl ^
    customtkinter ^
    reportlab ^
    python-dotenv ^
    Pillow ^
    --quiet

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Hubo un problema instalando alguna dependencia.
    echo Revisa tu conexion a internet e intentalo de nuevo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Instalacion completada exitosamente.
echo   Ejecuta main.py para iniciar el sistema.
echo ============================================
echo.
pause
