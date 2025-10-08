# job_posts/models.py
from django.db import models

class JobPost(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('closed', 'Closed'),
    ]

    # เก็บ ID จาก User Service และ Pet Service
    owner_id = models.IntegerField()
    pet_id = models.IntegerField()

    title = models.CharField(max_length=200)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"'{self.title}' by Owner ID: {self.owner_id}"