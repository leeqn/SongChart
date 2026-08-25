from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    tag= models.CharField(max_length=200)
    time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Songs"
        verbose_name = "Songs"