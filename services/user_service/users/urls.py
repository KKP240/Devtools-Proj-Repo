# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegisterView, UserProfileView, UserReadOnlyViewSet

# สร้าง router สำหรับ UserReadOnlyViewSet
router = DefaultRouter()
router.register(r'users', UserReadOnlyViewSet, basename='user')

urlpatterns = [
    # URL สำหรับจัดการ user profile
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('me/', UserProfileView.as_view(), name='user_profile'),

    # URL สำหรับ Simple JWT (Login, Refresh Token)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL ที่สร้างจาก router (สำหรับ /users/ และ /users/{id}/)
    path('', include(router.urls)),
]