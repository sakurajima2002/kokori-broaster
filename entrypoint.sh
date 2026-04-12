#!/bin/sh

set -e

echo "Generando migraciones..."
python manage.py makemigrations --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput


echo "Configurando administrador inicial..."
python manage.py setup_admin

exec "$@"
