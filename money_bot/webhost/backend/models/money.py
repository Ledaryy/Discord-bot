from django.db import models

class Money(models.Model):
    
    bot = models.ForeignKey(
        "Bot",
        verbose_name="money",
        on_delete=models.CASCADE
    )
    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.balance)