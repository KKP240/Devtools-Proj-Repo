from rest_framework import viewsets, permissions
from .models import JobPost
from .serializers import JobPostSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: return True
        return obj.owner_id == request.user.id

class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # แสดงเฉพาะโพสต์ที่ open สำหรับ public
        return JobPost.objects.filter(status='open').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)