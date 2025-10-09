from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [('P', 'pending'), ('C', 'confirmed'), ('X', 'cancelled'), ('D', 'done')]
    owner_id = models.IntegerField()
    caregiver_id = models.IntegerField()
    pet_id = models.IntegerField()
    proposal_id = models.IntegerField(unique=True, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    booking_id = models.IntegerField(unique=True)
    reviewer_id = models.IntegerField()
    reviewee_id = models.IntegerField()
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)