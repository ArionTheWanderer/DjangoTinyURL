from django.db import models


class Url(models.Model):
    short_url = models.SlugField(max_length=8, primary_key=True)
    long_url = models.URLField(max_length=100)
    clicks_number = models.IntegerField(default=0)

    def __str__(self):
        return self.long_url
