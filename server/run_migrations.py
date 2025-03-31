#!/usr/bin/env python
"""
Script to run migrations directly.
This can be executed on Render as: python run_migrations.py
"""
import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Set up Django environment
print("Setting up Django environment...")
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Check database connection
print("Checking database connection...")
db_conn = connections['default']
try:
    db_conn.cursor()
    print("Database connection successful!")
except OperationalError as e:
    print(f"Database connection error: {e}")
    sys.exit(1)

# Make migrations
print("Making migrations...")
try:
    from django.core.management import call_command
    call_command('makemigrations', 'submissions')
    print("Migrations created successfully!")
except Exception as e:
    print(f"Error creating migrations: {e}")

# Apply migrations
print("Applying migrations...")
try:
    call_command('migrate')
    print("Migrations applied successfully!")
except Exception as e:
    print(f"Error applying migrations: {e}")
    sys.exit(1)

print("Migration process completed successfully!") 