FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PORT=8000
ENV PYTHONPATH=/app/src

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry
RUN poetry config virtualenvs.create false

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies directly
RUN pip install -U pip && \
    pip install "django>=5.0.2,<6.0.0" \
    "djangorestframework>=3.14.0,<4.0.0" \
    "django-cors-headers>=4.3.1,<5.0.0" \
    "psycopg2-binary>=2.9.9,<3.0.0" \
    "dj-database-url>=2.1.0,<3.0.0" \
    "python-dotenv>=1.0.0,<2.0.0" \
    "gunicorn>=21.2.0,<22.0.0" \
    "gevent>=23.9.1,<24.0.0"

# Copy source code
COPY . .

# Run migrations
RUN cd src && python manage.py migrate || echo "Failed to run migrations during build"

# Expose the port
EXPOSE 8000

# Set the entrypoint
CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "core.wsgi:application"] 