#!/bin/bash

python manage.py migrate &&
python manage.py collectstatic --no-input &&

gunicorn webhost.wsgi -w 1 -b 0.0.0.0:80 --timeout 120 --workers 5 --worker-class gevent