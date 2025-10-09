from django.db import models

class Pet(models.Model):
    owner_id = models.IntegerField()
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.URLField(blank=True)