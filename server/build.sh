#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install poetry==1.7.1
poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi

echo "Making migrations..."
cd src
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!" 