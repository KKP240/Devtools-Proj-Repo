from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('P', 'pending'),
        ('C', 'confirmed'),
        ('X', 'cancelled'),
        ('D', 'done'),
    ]
    # เก็บ ID จาก User Service
    owner_id = models.IntegerField()
    caregiver_id = models.IntegerField()

    # เก็บ ID จาก Pet Service
    pet_id = models.IntegerField()
    
    # เก็บ ID จาก Proposal Service
    proposal_id = models.IntegerField(unique=True, null=True, blank=True)

    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for Pet ID: {self.pet_id}"

class Review(models.Model):
    # Booking อยู่ใน Service เดียวกัน จึงยังใช้ ForeignKey ได้
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    
    # ID ของผู้รีวิวและผู้ถูกรีวิว
    reviewer_id = models.IntegerField() 
    reviewee_id = models.IntegerField() # ปกติจะเป็น caregiver_id

    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking {self.booking.id} - Rating: {self.rating}"