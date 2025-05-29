#!/bin/bash

set -e

CONTAINER_1="back-tfg-api-principal-1"
CONTAINER_2="back-tfg-sorteos-api-1"
CONTAINER_3="back-tfg-noticiero-api-1"

echo "Ejecutando tests en el contenedor $CONTAINER_1..."
docker exec $CONTAINER_1 bash -c "cd /app/usuarios && pytest"

echo "Ejecutando tests en el contenedor $CONTAINER_2..."
docker exec $CONTAINER_2 bash -c "cd /app/sorteos && pytest"

echo "Ejecutando tests en el contenedor $CONTAINER_3..."
docker exec $CONTAINER_3 bash -c "cd /app/noticiero && python3 manage.py test"

echo "Tests completados correctamente en todos los contenedores."
