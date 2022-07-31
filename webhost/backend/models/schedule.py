from datetime import datetime, timedelta, timezone

from django.db import models
from django.utils import timezone as django_timezone


class TaskSchedule(models.Model):

    bot = models.OneToOneField(
        "Bot",
        related_name="task_schedule",
        on_delete=models.CASCADE,
    )

    next_collect_task = models.DateTimeField(blank=True, default=django_timezone.now)
    next_work_task = models.DateTimeField(blank=True, default=django_timezone.now)
    next_crime_task = models.DateTimeField(blank=True, default=django_timezone.now)

    def start_all(self):
        # Fixed delay for 180 seconds, needed for the first task
        delay = 180

        self.next_work_task = datetime.now(timezone.utc) + timedelta(seconds=delay)
        self.next_crime_task = datetime.now(timezone.utc) + timedelta(seconds=delay + 1)
        self.next_collect_task = datetime.now(timezone.utc) + timedelta(seconds=delay + 2)

        self.save()

    def get_eta_delay_for_hours(self, hours):
        import random
        from datetime import timedelta

        # Hardcoded 10 minutes delay
        minutes = 10

        # 0-30 minutes, 5 decimal places
        delay_seconds = round(random.uniform(15, 120), 5)
        eta = datetime.now(timezone.utc) + timedelta(hours=hours, minutes=minutes, seconds=delay_seconds)
        return eta

    def reschedule_work(self):
        self.next_work_task = self.get_eta_delay_for_hours(4)
        self.save()

    def reschedule_crime(self):
        self.next_crime_task = self.get_eta_delay_for_hours(4)
        self.save()

    def rechedule_collect(self):
        self.next_collect_task = self.get_eta_delay_for_hours(16)
        self.save()

    def get_schedule_display(self):
        template = "%b %d %X"
        return f"Work: {self.next_work_task.strftime(template)} \nCrime: {self.next_crime_task.strftime(template)} \nCollect: {self.next_collect_task.strftime(template)}"

    def __str__(self):
        return f"{self.bot} - work: {self.next_work_task} - crime: {self.next_crime_task} - collect: {self.next_collect_task}"
