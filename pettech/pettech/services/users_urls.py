from django.urls import path
from pettechApp import views

urlpatterns = [
    # Only expose user-centric API endpoints for this service
    path('api/me/', views.api_me, name='api_me'),
    # Reuse existing HTML auth routes if needed in monolith mode
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
