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
    path('caregiver/<int:pk>/', views.caregiver_detail, name='caregiver_detail'),
    path('caregiver/register/', views.caregiver_register, name='caregiver_register'),

    # Job Post URLs
    path('job-posts/create/', views.job_post_create, name='job_post_create'),
    path('job-posts/<int:pk>/', views.job_post_detail, name='job_post_detail'),

    # Proposal URLs
    path('job-posts/<int:job_post_id>/propose/', views.proposal_submit, name='proposal_submit'),
    path('job-posts/<int:job_post_id>/proposals/<int:proposal_id>/accept/', views.proposal_accept, name='proposal_accept'),

    # Booking URLs
    path('bookings/', views.booking_detail, name='booking_detail'),
    #path('bookings/<int:booking_id>/review/', views.review_create, name='review_create'),

    # User Profile URLs
    path('myprofile/', views.myprofile, name='myprofile'),
    path('booking-history/', views.my_booking_history, name='booking_history'),
    path('myposts/', views.myposts, name='myposts'),
    path('write_review/<int:booking_id>/', views.write_review, name='write_review'),

    # Authentication URLs
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]