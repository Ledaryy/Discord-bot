import random
from django.db import models
from datetime import datetime, timedelta, timezone


class TaskSchedule(models.Model):
    
    next_work_task = models.DateTimeField(auto_now_add=True)
    next_crime_task = models.DateTimeField(auto_now_add=True)
    next_collect_task = models.DateTimeField(auto_now_add=True)
    
    def start_all(self):
        # Fixed delay for 180 seconds, needed for the first task
        delay = 180
        
        delay = delay + random.randint(5, 10)
        self.next_work_task = datetime.now(timezone.utc) + timedelta(seconds=delay)
        
        delay = delay + random.randint(5, 10)
        self.next_crime_task = datetime.now(timezone.utc) + timedelta(seconds=delay)
        
        delay = delay + random.randint(5, 10)
        self.next_collect_task = datetime.now(timezone.utc) + timedelta(seconds=delay)
        
        self.save()
        
    def get_eta_delay_for_hours(self, hours):
        import random
        from datetime import timedelta

        # 0-30 minutes, 5 decimal places
        delay_seconds = round(random.uniform(0, 30), 5)
        eta = datetime.now(timezone.utc) + timedelta(hours=hours, seconds=delay_seconds)
        return eta
        
    def reschedule_work(self):
        self.next_work_task = self.get_eta_delay_for_hours(4)
        self.save()
        
    def reschedule_crime(self):
        self.next_crime_task = self.get_eta_delay_for_hours(4)
        self.save()
        
    def rechedule_collect(self):
        self.next_collect_task = self.get_eta_delay_for_hours(24)
        self.save()
        
    def __str__(self):
        return f"{self.bot} - work: {self.next_work_task} - crime: {self.next_crime_task} - collect: {self.next_collect_task}"