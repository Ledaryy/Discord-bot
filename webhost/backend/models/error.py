from django.db import models


class ErrorLog(models.Model):

    owner = models.ForeignKey("Bot", related_name="errors", on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    body = models.TextField(blank=True)

    def __str__(self):
        return f"{self.owner} - {self.date} - {self.comment}"
