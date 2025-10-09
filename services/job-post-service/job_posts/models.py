from django.db import models

class JobPost(models.Model):
    STATUS_CHOICES = [('open', 'Open'), ('assigned', 'Assigned'), ('closed', 'Closed')]
    owner_id = models.IntegerField()
    pet_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)