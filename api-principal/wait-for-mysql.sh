#!/bin/bash
# Espera hasta que MySQL esté disponible
while ! mysqladmin ping -h"mysql" --silent; do
  echo "Esperando a que MySQL esté disponible..."
  sleep 2
done

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
