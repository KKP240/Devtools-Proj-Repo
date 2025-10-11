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
    path('caregiver/<int:pk>/edit/', views.caregiver_edit, name='caregiver_edit'),

    # Job Post URLs
    path('job-posts/create/', views.job_post_create, name='job_post_create'),
    path('job-posts/<int:pk>/', views.job_post_detail, name='job_post_detail'),
    path('job-posts/<int:pk>/edit/', views.job_post_edit, name='job_post_edit'),
    path('job-posts/<int:pk>/delete/', views.job_post_delete, name='job_post_delete'),

    # Proposal URLs
    path('myproposals/', views.my_proposals, name='my_proposals'),
    path('job-posts/<int:job_post_id>/propose/', views.proposal_submit, name='proposal_submit'),
    path('job-posts/<int:job_post_id>/proposals/<int:proposal_id>/accept/', views.proposal_accept, name='proposal_accept'),

    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/complete/', views.booking_complete, name='booking_complete'), # for caregiver to mark as done
    #path('bookings/<int:booking_id>/review/', views.review_create, name='review_create'),

    # User Profile URLs
    path('myprofile/', views.myprofile, name='myprofile'),
    path('myprofile/edit/', views.edit_profile, name='edit_profile'),
    path('booking-history/', views.my_booking_history, name='booking_history'),
    path('myposts/', views.myposts, name='myposts'),
    path('write_review/<int:booking_id>/', views.write_review, name='write_review'),

    # Caregiver Profile
    path('caregiver-profile/<int:pk>/', views.caregiver_profile, name='caregiver_profile'),

    # User Profile
    #path('user/<int:pk>/', views.user_profile, name='user_profile'),

    # Authentication URLs
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    # API routes
    path('api/me/', views.api_me, name='api_me'),
    path('api/job-posts/', views.api_job_posts, name='api_job_posts'),
    path('api/job-posts/create/', views.api_job_post_create, name='api_job_post_create'),
    path('api/job-posts/<int:pk>/', views.api_job_post_detail, name='api_job_post_detail'),
    path('api/job-posts/<int:pk>/update/', views.api_job_post_update, name='api_job_post_update'),
    path('api/job-posts/<int:pk>/delete/', views.api_job_post_delete, name='api_job_post_delete'),
    path('api/job-posts/<int:job_post_id>/proposals/', views.api_proposal_submit, name='api_proposal_submit'),
    path('api/job-posts/<int:job_post_id>/proposals/<int:proposal_id>/accept/', views.api_proposal_accept, name='api_proposal_accept'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('api/bookings/<int:booking_id>/complete/', views.api_booking_complete, name='api_booking_complete'),
    path('api/booking-history/', views.api_booking_history, name='api_booking_history'),
    path('api/reviews/', views.api_review_create, name='api_review_create'),
    path('api/caregiver/<int:pk>/', views.api_caregiver_profile, name='api_caregiver_profile'),
    path('api/my-proposals/', views.api_my_proposals, name='api_my_proposals'),
]