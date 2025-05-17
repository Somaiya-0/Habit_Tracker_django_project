from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # each habit belongs to a user
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_done_today = models.BooleanField(default=False)

    def __str__(self):
        return self.name
