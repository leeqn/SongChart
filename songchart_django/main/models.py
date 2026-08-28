from django.db import models
import secrets
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    api_key = models.CharField(default=secrets.token_urlsafe, max_length=64, unique=True)
    def __str__(self):
        return f"Profile: {self.user.username}"

class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    tag= models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Songs"
        verbose_name = "Songs"