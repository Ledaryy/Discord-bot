#!/bin/bash
#
# Author: Andrew Kulishov <support@andrewkulishov.com>
# Copyright (C) 2022 Andrew Kulishov - All Rights Reserved
# 
# Created on Sun May 29 2022
# 
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# 
# If there are any issues contact me on the email above.
#

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate &&
python manage.py collectstatic --no-input --clear &&

gunicorn webhost.wsgi -w 1 -b 0.0.0.0:8000 --timeout 120 --workers 5 --worker-class gevent