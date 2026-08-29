#!/bin/bash
cd /home/site/wwwroot/songchart_django

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn --bind=0.0.0.0:8000 --timeout 600 songchart_django.wsgi:application