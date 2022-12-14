#!/usr/bin/env bash
(gunicorn stores_backend.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
(celery -A stores_backend worker --loglevel=INFO) & 
(celery -A stores_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler) &
(nginx -g "daemon off;")