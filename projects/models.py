from django.db import models
from django.utils.crypto import get_random_string


class Project(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200, unique=True)
    image = models.ImageField(blank=True, upload_to='project/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            random_integer = get_random_string(length=5, allowed_chars='0123456789')
            self.id = f'{self.link}-{random_integer}'
        super().save(*args, **kwargs)
