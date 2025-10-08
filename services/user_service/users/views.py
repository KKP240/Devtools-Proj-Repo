# users/views.py
from rest_framework import generics, permissions, viewsets
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserDetailSerializer

class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint for creating a new user. Publicly accessible.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny] # อนุญาตให้ทุกคนเข้าถึงได้เพื่อสมัครสมาชิก
    serializer_class = UserRegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for the logged-in user to view and update their profile.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # คืนค่า user object ของคนที่ login อยู่เสมอ
        return self.request.user

class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A public viewset for viewing users. Other services can use this
    to get public user information.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny] # อนุญาตให้ทุกคนดูข้อมูล public ได้