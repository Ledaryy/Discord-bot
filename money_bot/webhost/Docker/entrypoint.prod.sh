#!/bin/bash

python manage.py migrate &&
python manage.py collectstatic --no-input --clear &&

gunicorn webhost.wsgi -w 1 -b 0.0.0.0:8000 --timeout 120 --workers 5 --worker-class gevent