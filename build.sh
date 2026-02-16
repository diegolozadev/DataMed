#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

python manage.py createsuperuser --noinput || true

echo "LOG: Verificando estado de la base de datos..."
python manage.py showmigrations

echo "LOG: Intentando migrar..."
python manage.py migrate --noinput

echo "LOG: Verificando si las tablas se crearon..."
python manage.py inspectdb | head -n 20