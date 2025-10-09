from django.db import models

class Proposal(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]
    job_post_id = models.IntegerField()
    caregiver_id = models.IntegerField()
    message = models.TextField(blank=True)
    proposed_rate = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)