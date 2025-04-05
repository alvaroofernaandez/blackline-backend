#!/bin/bash
echo "Esperando a que MySQL esté disponible..."

while ! nc -z mysql 3306; do
  sleep 1
done

echo "MySQL está disponible. Arrancando servidor Django..."
exec "$@"
