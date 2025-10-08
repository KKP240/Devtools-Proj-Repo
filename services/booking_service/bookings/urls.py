# bookings_service/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ReviewViewSet

# สร้าง router และลงทะเบียน ViewSet
router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

# URL urlpatterns จะถูกสร้างโดย router โดยอัตโนมัติ
urlpatterns = [
    path('', include(router.urls)),
]