#!/bin/bash
#
# Author: Andrew Kulishov <support@andrewkulishov.com>
# Copyright (C) 2022 Andrew Kulishov - All Rights Reserved
#
# Created on Sat May 28 2022
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
#
# If there are any issues contact me on the email above.
#


python manage.py collectstatic --no-input &
python manage.py makemigrations &&
python manage.py migrate &&
# python manage.py createsuperuser --noinput &&

python manage.py runserver 0.0.0.0:8000