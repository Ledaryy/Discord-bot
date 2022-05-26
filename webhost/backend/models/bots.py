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
    
    balance = models.OneToOneField(
        "Balance",
        related_name="bot",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    schedule = models.OneToOneField(
        "TaskSchedule",
        related_name="bot",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
        

    def __str__(self):
        return self.name

    def start(self, delay=0):
        # Starts auto collect chain
        celery.current_app.send_task(
            "backend.tasks.start_bot", args=(self.id, delay))

    def stop(self, delay=0):
        # Stops auto collect chain
        celery.current_app.send_task(
            "backend.tasks.stop_bot", args=(self.id, delay))

    def save(self, *args, **kwargs):
        if not self.balance:
            self.balance = Balance.objects.create()
            self.balance.save()
        if not self.schedule:
            self.schedule = TaskSchedule.objects.create()
            self.schedule.save()
        super().save(*args, **kwargs)
