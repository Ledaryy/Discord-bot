from django.db import models

class Bot(models.Model):
    
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    balance = models.ForeignKey("backend.Money", verbose_name="bot", on_delete=models.CASCADE)