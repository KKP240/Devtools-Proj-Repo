from django.urls import path
from pettechApp import views

urlpatterns = [
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('api/bookings/<int:booking_id>/complete/', views.api_booking_complete, name='api_booking_complete'),
    path('api/booking-history/', views.api_booking_history, name='api_booking_history'),
    path('api/reviews/', views.api_review_create, name='api_review_create'),
    path('api/caregiver/<int:pk>/', views.api_caregiver_profile, name='api_caregiver_profile'),
]
