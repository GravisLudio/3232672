@echo off
chcp 65001 >nul
title Instalador CRS v2.0

echo ============================================
echo   CHRONOS REGISTRY SYSTEM -- Instalador
echo   SENA CIDM - Ficha 3232672
echo ============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detectado:
python --version
echo.

echo [1/4] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo     pip no encontrado. Instalando con ensurepip...
    python -m ensurepip --upgrade
)
python -m pip install --upgrade pip --quiet
echo     pip listo.
echo.

echo [2/4] Instalando bcrypt...
python -m pip install bcrypt --only-binary :all: --quiet
if %errorlevel% neq 0 (
    python -m pip install bcrypt --quiet
)
echo     bcrypt listo.
echo.

echo [3/4] Instalando dependencias...
python -m pip install mysql-connector-python pandas tkcalendar openpyxl customtkinter reportlab python-dotenv Pillow --quiet
echo.

echo [4/4] Verificando instalacion...
python -c "import bcrypt, customtkinter, pandas, tkcalendar, openpyxl, reportlab, dotenv, PIL; print('[OK] Todas las dependencias instaladas correctamente')"
if %errorlevel% neq 0 (
    echo [ERROR] Alguna dependencia no se instalo bien. Revisa tu conexion a internet.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Instalacion completada exitosamente.
echo   Ejecuta iniciar_CRS.bat para abrir CRS.
echo ============================================
echo.
pause