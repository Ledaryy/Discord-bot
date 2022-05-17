import celery
from django.db import models


class Bot(models.Model):

    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def work(self):
        # Starts auto collect chain
        celery.send_task("backend.tasks.start_collect", args=(self.id,))
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
