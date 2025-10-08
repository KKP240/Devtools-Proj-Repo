from rest_framework import viewsets, permissions
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        uid = getattr(request.user, 'id', None)
        return uid in (obj.owner_id, obj.caregiver_id)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]
