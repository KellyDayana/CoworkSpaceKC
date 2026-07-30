#!/usr/bin/env bash
set -o errexit

echo "===== INSTALANDO DEPENDENCIAS ====="
pip install -r requirements.txt

echo "===== RECOPILANDO ARCHIVOS ESTÁTICOS ====="
python manage.py collectstatic --noinput

echo "===== EJECUTANDO MIGRACIONES ====="
python manage.py migrate

echo "===== CREANDO SUPERUSUARIO ====="
python manage.py crear_superusuario

echo "===== BUILD COMPLETADO ====="
