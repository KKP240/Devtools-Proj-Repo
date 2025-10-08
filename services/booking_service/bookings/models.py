from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'pending'),
        ('C', 'confirmed'),
        ('X', 'cancelled'),
        ('D', 'done'),
    ]
    owner_id = models.IntegerField()
    caregiver_id = models.IntegerField()
    pet_id = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
