#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install poetry
poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi

# Run migrations
python src/manage.py migrate

# Collect static files
python src/manage.py collectstatic --no-input 