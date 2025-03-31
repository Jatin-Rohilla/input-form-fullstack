#!/usr/bin/env python
"""
Script to run migrations directly.
This can be executed on Render as: python run_migrations.py
"""
import os
import sys
import django
import time
import traceback
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError

# Set up Django environment
print("Setting up Django environment...")
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    django.setup()
    print("Django setup successful!")
except Exception as e:
    print(f"Django setup failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Display database settings
from django.conf import settings
print(f"Database settings: {settings.DATABASES['default']}")

# Check database connection
print("Checking database connection...")
db_conn = connections['default']

# Retry connection a few times
max_retries = 5
retry_delay = 3  # seconds

for attempt in range(max_retries):
    try:
        db_conn.cursor()
        print("Database connection successful!")
        break
    except OperationalError as e:
        if attempt < max_retries - 1:
            print(f"Database connection error (attempt {attempt+1}/{max_retries}): {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed to connect to database after {max_retries} attempts: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected database error: {e}")
        traceback.print_exc()
        sys.exit(1)

# List existing tables
print("Checking existing tables...")
try:
    with connections['default'].cursor() as cursor:
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"Existing tables: {tables}")
        else:
            print("Not a PostgreSQL database, skipping table check.")
except Exception as e:
    print(f"Error checking tables: {e}")

# Make migrations
print("Making migrations...")
try:
    from django.core.management import call_command
    # First try creating the submissions app migrations
    call_command('makemigrations', 'submissions', '--noinput', verbosity=2)
    print("Submissions app migrations created successfully!")
    
    # Then create all other necessary migrations
    call_command('makemigrations', '--noinput', verbosity=2)
    print("All migrations created successfully!")
except Exception as e:
    print(f"Error creating migrations: {e}")
    traceback.print_exc()
    # Continue anyway, as migrations might already exist

# Apply migrations
print("Applying migrations...")
try:
    call_command('migrate', '--noinput', verbosity=2)
    print("Migrations applied successfully!")
except ProgrammingError as e:
    print(f"ProgrammingError during migration: {e}")
    traceback.print_exc()
    print("This might be due to missing tables. Trying with --fake-initial...")
    try:
        call_command('migrate', '--fake-initial', '--noinput', verbosity=2)
        print("Migrations with --fake-initial applied successfully!")
    except Exception as e2:
        print(f"Error applying migrations with --fake-initial: {e2}")
        traceback.print_exc()
        sys.exit(1)
except Exception as e:
    print(f"Error applying migrations: {e}")
    traceback.print_exc()
    sys.exit(1)

# Check if the submissions_formsubmission table exists now
print("Checking if submissions_formsubmission table exists...")
try:
    with connections['default'].cursor() as cursor:
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            cursor.execute("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE table_schema = 'public' 
                   AND table_name = 'submissions_formsubmission'
                );
            """)
            exists = cursor.fetchone()[0]
            if exists:
                print("submissions_formsubmission table exists!")
            else:
                print("submissions_formsubmission table does NOT exist! Migration failed.")
                sys.exit(1)
        else:
            print("Not a PostgreSQL database, skipping table check.")
except Exception as e:
    print(f"Error checking submissions_formsubmission table: {e}")
    traceback.print_exc()

print("Migration process completed successfully!") 