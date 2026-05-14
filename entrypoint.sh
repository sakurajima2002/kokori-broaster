#!/bin/sh

set -e

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Generando migraciones desde modelos..."
python manage.py makemigrations --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Sincronizando parámetros del sitio (solo crea claves faltantes)..."
python manage.py sync_site_parameters

echo "Configurando administrador inicial..."
python manage.py setup_admin

exec "$@"
