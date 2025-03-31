FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
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

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies with explicit Python version
RUN poetry config virtualenvs.create false && \
    poetry env use python3.10 && \
    poetry install --no-interaction --no-ansi --no-root

# Copy source code
COPY . .

# Run migrations
RUN cd src && python manage.py migrate || echo "Failed to run migrations during build"

# Expose the port
EXPOSE 8000

# Set the entrypoint
CMD ["poetry", "run", "gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "core.wsgi:application"] 