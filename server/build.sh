#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -U pip
pip install "django>=5.0.2,<6.0.0" \
    "djangorestframework>=3.14.0,<4.0.0" \
    "django-cors-headers>=4.3.1,<5.0.0" \
    "psycopg2-binary>=2.9.9,<3.0.0" \
    "dj-database-url>=2.1.0,<3.0.0" \
    "python-dotenv>=1.0.0,<2.0.0" \
    "gunicorn>=21.2.0,<22.0.0" \
    "gevent>=23.9.1,<24.0.0"

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