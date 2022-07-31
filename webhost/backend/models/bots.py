import celery
from django.db import models

from .money import Balance
from .schedule import TaskSchedule


class BotRoles(models.TextChoices):
    disabled = "disabled", "disabled"
    collecter = "collecter", "collecter"
    bumper = "bumper", "bumper"
    collecter_and_bumper = "collecter_and_bumper", "collecter_and_bumper"


class Bot(models.Model):

    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    role = models.CharField(
        max_length=100,
        choices=BotRoles.choices,
        default=BotRoles.disabled,
    )

    def __str__(self):
        return self.name

    def start(self, delay=0):
        # Starts auto collect chain
        celery.current_app.send_task("backend.tasks.start_bot", args=(self.id, delay))

    def stop(self, delay=0):
        # Stops auto collect chain
        celery.current_app.send_task("backend.tasks.stop_bot", args=(self.id, delay))

    def send_message(self, message, delay=0):
        # Send message to the chat
        celery.current_app.send_task("backend.tasks.send_message", args=(self.id, message, delay))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Move to the create function

        try:
            self.balance
        except Balance.DoesNotExist:
            self.balance = Balance.objects.create(bot=self)
            self.balance.save()

        try:
            self.task_schedule
        except TaskSchedule.DoesNotExist:
            self.task_schedule = TaskSchedule.objects.create(bot=self)
            self.task_schedule.save()
