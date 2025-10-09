from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MyProfileView, UserReadOnlyViewSet

router = DefaultRouter()
router.register(r'users', UserReadOnlyViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('myprofile/', MyProfileView.as_view(), name='myprofile'),
    path('login/', TokenObtainPairView.as_view(), name='login'), # simplejwt จะใช้ username/password เป็น default
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]