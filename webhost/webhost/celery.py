from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webhost.settings")
app = Celery("webhost")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "every_1_min_check_and_send_tasks_from_db": {
        "task": "backend.tasks.schedule_tasks",
        "schedule": crontab(hour="*", minute="*", day_of_week="*"),
    }
}

app.conf.timezone = "UTC"
