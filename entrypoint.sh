#!/bin/sh

set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput


echo "Configurando administrador inicial..."
python manage.py setup_admin

exec "$@"
