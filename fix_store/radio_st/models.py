from django.db import models
from django.urls import reverse


class Radios(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('radio')
