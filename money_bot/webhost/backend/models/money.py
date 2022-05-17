from django.db import models

class MoneyLog(models.Model):
    
    owner = models.OneToOneField(
        "Bot",
        related_name="money",
        on_delete=models.CASCADE
    )
    earned = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.owner} - {self.date} - {self.earned}"