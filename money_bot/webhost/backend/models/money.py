from django.db import models

class Money(models.Model):
    
    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    