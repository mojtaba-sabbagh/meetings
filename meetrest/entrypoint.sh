#!/bin/sh

python manage.py migrate --no-input

gunicorn meetrest.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 0.0.0.0:8000
mkdir -p /app/static
python manage.py collectstatic