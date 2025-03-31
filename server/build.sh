#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install poetry==1.7.1
poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi

echo "Making migrations..."
cd src
python manage.py makemigrations submissions --noinput || echo "Failed to make migrations, may already exist"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python -c "
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print('Superuser created.')
    else:
        print('Superuser already exists.')
except IntegrityError:
    print('Superuser already exists.')
except Exception as e:
    print(f'Error creating superuser: {e}')
" || echo "Could not create superuser"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!" 