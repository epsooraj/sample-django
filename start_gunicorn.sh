#!/bin/bash
# Gunicorn startup script for Django application

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn sampleapp.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

