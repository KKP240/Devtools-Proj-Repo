# pet_service/views.py
from rest_framework import viewsets, permissions
from .models import Pet
from .serializers import PetSerializer
from django.views.decorators.csrf import csrf_exempt

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # อนุญาตให้เจ้าของ (คนที่ user.id ตรงกับ owner_id ของ pet)
        # สามารถแก้ไขหรือลบข้อมูลได้
        return obj.owner_id == request.user.id

class PetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pets to be viewed or edited.
    """
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        """
        ผู้ใช้จะสามารถมองเห็นสัตว์เลี้ยงของตัวเองเท่านั้น
        """
        user = self.request.user
        return Pet.objects.filter(owner_id=user.id)

    def perform_create(self, serializer):
        """
        ตอนสร้างสัตว์เลี้ยงใหม่ ให้บันทึก owner_id เป็น id ของผู้ใช้ที่ login อยู่โดยอัตโนมัติ
        """
        serializer.save(owner_id=self.request.user.id)