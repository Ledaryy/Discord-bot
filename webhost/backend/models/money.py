from django.db import models


class MoneyLog(models.Model):

    owner = models.ForeignKey(
        "Bot",
        related_name="money",
        on_delete=models.CASCADE
    )
    earned = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.owner} - {self.date} - {self.earned} - {self.comment}"

    def save(self, *args, **kwargs):

        # Update owner's balance
        self.owner.balance += self.earned
        self.owner.total_earned += self.earned

        self.owner.save()

        super().save(*args, **kwargs)
