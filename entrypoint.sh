#!/bin/bash

# Wait for MySQL to be available
/wait-for-it.sh db:3306 --timeout=60 --strict -- echo "MySQL is up - executing command"

# Apply migrations and collect static files
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 CRUD.wsgi:application
