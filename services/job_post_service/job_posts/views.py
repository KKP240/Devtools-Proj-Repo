# job_posts/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobPost
from .serializers import JobPostSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    อนุญาตให้ทุกคนอ่านได้ แต่จะให้แก้ไขได้เฉพาะเจ้าของเท่านั้น
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner_id == request.user.id

class JobPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Job Posts.
    """
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        โดยปกติจะแสดงเฉพาะโพสต์ที่ 'open' เท่านั้น
        """
        return JobPost.objects.filter(status='open').order_by('-created_at')

    def perform_create(self, serializer):
        """
        กำหนดเจ้าของโพสต์เป็น user ที่ login อยู่โดยอัตโนมัติ
        """
        # ในระบบจริง ควรมีการตรวจสอบก่อนว่า pet_id ที่ส่งมาเป็นของ user คนนี้จริงๆ
        # โดยการยิง API ไปถามที่ pet_service
        serializer.save(owner_id=self.request.user.id)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """
        Endpoint สำหรับดูโพสต์ทั้งหมดของตัวเอง
        """
        my_posts = JobPost.objects.filter(owner_id=request.user.id).order_by('-created_at')
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data)