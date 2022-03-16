web: gunicorn CRUD.wsgi
worker: celery -A CRUD worker
beat: celery -A CRUD beat