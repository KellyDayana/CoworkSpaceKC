#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Marcar todas las migraciones existentes como aplicadas sin ejecutarlas
python manage.py migrate --fake

# Aplicar cualquier migración nueva real
python manage.py migrate
