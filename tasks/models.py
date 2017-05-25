from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.task
