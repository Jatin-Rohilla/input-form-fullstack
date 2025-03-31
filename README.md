# Input Form Fullstack Application

A fullstack application with a React frontend and Django+PostgreSQL backend.

## Project Structure

- `client/`: React frontend application
- `server/`: Django backend application

## Frontend (React + Vite)

The frontend is a React application built with Vite, featuring:

- Form for collecting user information
- Table view for displaying submissions
- Integration with the backend API

### Running the Frontend

```bash
cd client
npm install
npm run dev
```

The development server will start at `http://localhost:5173`.

## Backend (Django + PostgreSQL)

The backend is a Django application with PostgreSQL database, using:

- Django REST Framework for API
- Poetry for dependency management
- Docker for containerization

### Running the Backend with Docker

```bash
cd server
docker-compose up
```

This will start both the Django application and PostgreSQL database.

The API will be available at `http://localhost:8000/api/`.

### Setting Up the Backend Manually

1. Install Poetry

   ```bash
   pip install poetry
   ```

2. Install dependencies

   ```bash
   cd server
   poetry install
   ```

3. Run migrations

   ```bash
   cd server
   poetry run python src/manage.py migrate
   ```

4. Start the development server
   ```bash
   cd server
   poetry run python src/manage.py runserver
   ```

## Deployment

### Frontend (Vercel)

The frontend is configured for deployment on Vercel.

1. Connect your GitHub repository to Vercel
2. Set environment variables:
   - `VITE_API_URL`: URL of your deployed backend API

### Backend (Render)

The backend is configured for deployment on Render.

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure as a Python application with:
   - Build Command: `./build.sh`
   - Start Command: `cd src && gunicorn core.wsgi:application`
4. Add environment variables:

   - `DEBUG`: False
   - `SECRET_KEY`: Your secure secret key
   - `ALLOWED_HOSTS`: Your Render domain, e.g., `your-app.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: Your Vercel frontend URL, e.g., `https://your-frontend.vercel.app`
   - `DATABASE_URL`: Will be automatically set by Render if you attach a PostgreSQL database

5. Create a PostgreSQL database on Render and link it to your web service
