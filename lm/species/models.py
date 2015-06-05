from django.db import models

class Species(models.Model):
    species = models.CharField(max_length=100, blank=False)
    specimens = models.PositiveIntegerField(default=0, blank=False)

    class Meta:
        ordering = ('species','specimens')
