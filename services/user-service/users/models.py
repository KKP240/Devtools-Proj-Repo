from django.db import models
from django.contrib.auth.models import User # <-- import User ปกติ

class CaregiverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caregiver_profile')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    area = models.CharField(max_length=100, blank=True)
    available_days = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"