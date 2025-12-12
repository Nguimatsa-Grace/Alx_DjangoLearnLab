# Deployment Documentation

## Hosting Service
- **Provider:** Render / Heroku (Choose one)
- **URL:** [Insert your Live URL here]

## Environment Setup
1. Installed `gunicorn` and `whitenoise` for production web serving and static files.
2. Configured `django-environ` to handle secret keys and database URLs.
3. Added a `Procfile` for the application process manager.

## Database
- Production uses a PostgreSQL database provided by the hosting service.
- Local development continues to use SQLite.

## Static Files
- Managed via `WhiteNoise` to serve CSS/JS directly from the application server.
