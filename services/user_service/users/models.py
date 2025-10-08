# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # เราใช้ email เป็น field สำหรับ login แทน username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # username ยังต้องมี แต่ใช้ login ไม่ได้

    def __str__(self):
        return self.email

class CaregiverProfile(models.Model):
    # เชื่อมโยงกับ CustomUser แบบ One-to-One
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='caregiver_profile')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True)
    # เก็บวันว่างงานเป็น JSON Array เช่น ["Monday", "Wednesday"]
    available_days = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"