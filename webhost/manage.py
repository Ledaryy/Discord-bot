#!/usr/bin/env python

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


import os
import sys
from time import sleep

from django.core.checks import Error
from django.db import connections


def check_postgres(**kwargs):
    errors = []
    for name in connections:
        cursor = connections[name].cursor()
        cursor.execute("SELECT 1;")
        row = cursor.fetchone()
        if row is None:
            errors.append(Error("Postgres connection failed", hint="Check your postgres settings", id="webhost.E001"))
    return errors


def startup_check():
    while True:
        error = check_postgres()
        sleep(1)
        if not error:
            break
        else:
            print("Postgres connection failed")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webhost.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    startup_check()

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
