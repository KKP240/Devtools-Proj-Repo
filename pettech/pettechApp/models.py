from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_caregiver = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)

class Pet(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    photo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.species})"

class CaregiverProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='caregiver_profile')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    area = models.CharField(max_length=100, blank=True)
    available_days = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Caregiver: {self.user.username}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'pending'),
        ('C', 'confirmed'),
        ('X', 'cancelled'),
        ('D', 'done'),
    ]
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookings')
    caregiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='jobs')
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} ({self.owner} -> {self.caregiver})"

class Review(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
