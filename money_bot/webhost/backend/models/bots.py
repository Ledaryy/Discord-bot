import celery
from django.db import models


class BotTypes(models.TextChoices):
    disabled = "disabled", "disabled"
    collecter = "collecter", "collecter"
    bumper = "bumper", "bumper"
    collecter_and_bumper = "collecter_and_bumper", "collecter_and_bumper"

class Bot(models.Model):

    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    bot_type = models.CharField(
        max_length=100,
        choices=BotTypes.choices,
        default=BotTypes.disabled,
    )

    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def start(self, delay=0):
        # Starts auto collect chain
        celery.current_app.send_task("backend.tasks.start_collect", args=(self.id, delay))

    def stop(self, delay=0):
        # Stops auto collect chain
        celery.current_app.send_task("backend.tasks.stop_collect", args=(self.id, delay))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
