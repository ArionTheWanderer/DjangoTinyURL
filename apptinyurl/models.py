from django.db import models
from django.conf import settings


class Url(models.Model):
    short_url = models.SlugField(max_length=settings.SHORT_URL_LENGTH, primary_key=True)
    long_url = models.URLField(max_length=100)
    clicks_number = models.IntegerField(default=0)

    def __str__(self):
        return self.long_url
