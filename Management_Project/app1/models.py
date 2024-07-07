from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the built-in User model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} (Batch: {self.batch_name})"
