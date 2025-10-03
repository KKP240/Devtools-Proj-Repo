from django.urls import path
from . import views

urlpatterns = [
    # พี่เลี้ยงจอง

    # Home แสดง posts ของทุกคน มีปุ่มให้เพิ่ม posts ใหม่
    # My posts 
    # createPosts, editPosts
    # userProfile
    # postDetail
    # bookings
    # bookingHistory


    # Auth
    path('', views.home, name='home'),
    path('caregivers/', views.caregiver_list, name='caregiver_list'),
    path('caregiver/<int:pk>/', views.caregiver_detail, name='caregiver_detail'),
    path('pet/', views.pet_list, name='pet_list'),

    path('pets/add/', views.pet_add, name='pet_add'),

    path('booking/create/<int:caregiver_id>/', views.booking_create, name='booking_create'),
    path('bookings/', views.my_bookings, name='my_bookings'),

    # auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
