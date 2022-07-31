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

# from django.contrib.auth.models import AbstractUser
# from django.core.management.base import BaseCommand

# TODO rework this
# class Command(BaseCommand):
#     help = "Initialize admin user (only for development)"

#     def handle(self, *args, **options):
#         if not AbstractUser.objects.filter(username="root").exists():
#             AbstractUser.objects.create_superuser(
#                 "root", "root@example.com", "123456"
#             )
#             print(
#                 "Superuser created. Username: root, password: 123456"
#             )
#         else:
#             print("Admin Account Already Exists")
