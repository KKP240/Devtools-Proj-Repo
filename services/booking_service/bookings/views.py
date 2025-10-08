# bookings_service/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

# อาจจะต้องสร้าง Permission class นี้ขึ้นมาเพื่อตรวจสอบความเป็นเจ้าของ
# ในตัวอย่างนี้จะใช้ IsAuthenticated ไปก่อน
class IsBookingParticipant(permissions.BasePermission):
    """
    อนุญาตให้เฉพาะ owner หรือ caregiver ของ booking เข้าถึงได้
    """
    def has_object_permission(self, request, view, obj):
        # ในระบบจริง ควรจะมีการส่ง User ID มากับ Token
        # สมมติว่าได้ user_id มาจาก request
        user_id = request.user.id 
        return user_id in (obj.owner_id, obj.caregiver_id)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingParticipant]

    def get_queryset(self):
        """
        Filter ให้ผู้ใช้เห็นเฉพาะ booking ของตัวเอง
        """
        user_id = self.request.user.id
        return Booking.objects.filter(models.Q(owner_id=user_id) | models.Q(caregiver_id=user_id))

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsBookingParticipant])
    def complete(self, request, pk=None):
        """
        Action สำหรับ caregiver เพื่อเปลี่ยนสถานะ booking เป็น 'done'
        """
        booking = self.get_object()
        if booking.status != 'C': # Confirmed
            return Response({'error': 'Booking is not confirmed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'D' # Done
        booking.save()
        return Response(BookingSerializer(booking).data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        เมื่อมีการสร้าง Review ให้ดึง ID ของผู้รีวิวและผู้ถูกรีวิวจาก Booking
        """
        booking = get_object_or_404(Booking, pk=self.request.data.get('booking'))
        
        # ตรวจสอบว่าผู้สร้างรีวิวเป็น owner ของ booking
        if self.request.user.id != booking.owner_id:
            raise permissions.PermissionDenied("You are not the owner of this booking.")

        # ตรวจสอบว่า booking เสร็จสิ้นแล้ว (status 'D')
        if booking.status != 'D':
             raise permissions.PermissionDenied("You can only review completed bookings.")

        serializer.save(reviewer_id=booking.owner_id, reviewee_id=booking.caregiver_id)