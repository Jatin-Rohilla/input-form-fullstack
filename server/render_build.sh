#!/bin/bash
# Specialized build script for Render.com

set -o errexit

# Install dependencies directly with pip
echo "Installing dependencies with pip..."
pip install -U pip
pip install "django>=5.0.2,<6.0.0" \
    "djangorestframework>=3.14.0,<4.0.0" \
    "django-cors-headers>=4.3.1,<5.0.0" \
    "psycopg2-binary>=2.9.9,<3.0.0" \
    "dj-database-url>=2.1.0,<3.0.0" \
    "python-dotenv>=1.0.0,<2.0.0" \
    "gunicorn>=21.2.0,<22.0.0" \
    "gevent>=23.9.1,<24.0.0"

# Change to the src directory
cd src

# Create initial migrations
echo "Creating migrations..."
python manage.py makemigrations submissions --noinput || echo "Failed to create migrations"

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput || echo "Failed to apply migrations, will try run_migrations.py"

# If migrations failed, try the more robust migration script
if [ $? -ne 0 ]; then
    echo "Using backup migration script..."
    cd ..
    python run_migrations.py
    cd src
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!" 