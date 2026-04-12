#!/bin/sh

set -e

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Generando migraciones..."
python manage.py makemigrations --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput


echo "Configurando administrador inicial..."
python manage.py setup_admin

exec "$@"
