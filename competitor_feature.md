# Vercel Feature: Zero-configuration Django Support

**Release Date:** April 9, 2026
**Framework:** Django (Python)

## Core Technical Requirements & Specifications

### 1. Platform & Compute Requirements
- **Compute Model:** Uses Vercel's *Fluid compute* architecture with Active CPU pricing by default.
- **Static Asset Serving:** Static files are automatically detected and served globally via the Vercel CDN without manual configuration.

### 2. Required File Structure
Vercel automatically detects the framework if the standard Django file structure is present. Developers no longer need to rely on `vercel.json` redirects or an `/api` directory.
- `manage.py`: The CLI entry point for the application.
- `app/settings.py`: The project settings file.
- `app/urls.py`: The URL routing table.
- `app/wsgi.py`: The WSGI entry point for handling requests.

### 3. Application Entry Point (WSGI)
The platform uses the standard WSGI application instance. The `app/wsgi.py` file must expose the `application` object properly:
```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()
```

### 4. Configuration (settings.py)
Django settings generally remain standard, with the crucial requirement that `.vercel.app` (or custom domains) must be permitted in `ALLOWED_HOSTS`:
```python
SECRET_KEY = "your-secret-key"
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"]
ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"
INSTALLED_APPS = ["app"]
```

### 5. Deployment Mechanism
Deploying requires no specialized commands beyond standard Vercel CLI usage (`vercel deploy`) or pushing to a connected Git integration. Vercel's build system autonomously parses the Python environment and Django setup.
