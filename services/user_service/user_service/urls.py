from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ลบ path ของ token เดิมออก
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # เพิ่มบรรทัดนี้:
    # บอก Django ว่า ถ้ามี URL ที่ขึ้นต้นด้วย "api/"
    # ให้ส่งต่อไปให้ไฟล์ urls.py ของแอปที่ชื่อ 'users' เป็นคนจัดการ
    path('api/', include('users.urls')),
]