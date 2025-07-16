#!/bin/bash
# run_docker.sh - Script para ejecutar procesamiento YOLO en Linux/Mac

echo "[$(date)] Iniciando procesamiento YOLO..."

# Verificar si Docker está disponible
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker no está instalado o no está en el PATH"
    exit 1
fi

# Verificar si la imagen existe
if ! docker images | grep -q "mi-yolo-app"; then
    echo "ERROR: La imagen 'mi-yolo-app' no existe"
    echo "Construye la imagen con: docker build -t mi-yolo-app ."
    exit 1
fi

# Crear directorios si no existen
mkdir -p input output

echo "[$(date)] Ejecutando contenedor Docker..."

# Ejecutar Docker con montaje de volúmenes
docker run --rm \
    -v "$(pwd)/input:/app/input" \
    -v "$(pwd)/output:/app/output" \
    mi-yolo-app

# Capturar código de salida
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "[$(date)] Procesamiento completado exitosamente"
else
    echo "[$(date)] Error en el procesamiento. Código: $exit_code"
fi

exit $exit_code