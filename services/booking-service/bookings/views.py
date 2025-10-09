from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Booking.objects.filter(Q(owner_id=user_id) | Q(caregiver_id=user_id))

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # แสดงเฉพาะรีวิวที่ตัวเองเขียน หรือถูกเขียนถึง
        user_id = self.request.user.id
        return Review.objects.filter(Q(reviewer_id=user_id) | Q(reviewee_id=user_id))

    def perform_create(self, serializer):
        # Logic สำหรับการสร้าง review จะต้องซับซ้อนกว่านี้
        # เช่น ตรวจสอบว่าเป็นเจ้าของ booking จริงหรือไม่
        # แต่เพื่อความง่าย จะบันทึกไปก่อน
        serializer.save(reviewer_id=self.request.user.id)