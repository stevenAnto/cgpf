@echo off
REM run_docker.bat - Script para ejecutar procesamiento YOLO en Windows

echo [%date% %time%] Iniciando procesamiento YOLO...

REM Verificar si Docker está disponible
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no está instalado o no está en el PATH
    exit /b 1
)

REM Verificar si la imagen existe
docker images mi-yolo-app | find "mi-yolo-app" >nul
if %errorlevel% neq 0 (
    echo ERROR: La imagen 'mi-yolo-app' no existe
    echo Construye la imagen con: docker build -t mi-yolo-app .
    exit /b 1
)

REM Crear directorios si no existen
if not exist "input" mkdir input
if not exist "output" mkdir output

echo [%date% %time%] Ejecutando contenedor Docker...

REM Ejecutar Docker con montaje de volúmenes
docker run --rm ^
    -v "%cd%/input:/app/input" ^
    -v "%cd%/output:/app/output" ^
    mi-yolo-app

REM Capturar código de salida
set exit_code=%errorlevel%

if %exit_code% equ 0 (
    echo [%date% %time%] Procesamiento completado exitosamente
) else (
    echo [%date% %time%] Error en el procesamiento. Código: %exit_code%
)

exit /b %exit_code%