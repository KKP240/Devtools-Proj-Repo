from django.db import models

class Pet(models.Model):
    owner_id = models.IntegerField()  # store user id from user_service
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.species})"
