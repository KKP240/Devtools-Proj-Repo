from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

# สร้าง router
router = DefaultRouter()

# ลงทะเบียนด้วย "ชื่อคลาส" โดยตรง ไม่ต้องมี .as_view()
# และแนะนำให้ใส่ basename เพื่อความชัดเจน
router.register(r'pets', PetViewSet, basename='pet')

# urlpatterns จะใช้ URL ที่ router สร้างให้
urlpatterns = [
    path('', include(router.urls)),
]