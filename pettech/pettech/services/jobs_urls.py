from django.urls import path
from pettechApp import views

urlpatterns = [
    # API: Job posts
    path('api/job-posts/', views.api_job_posts, name='api_job_posts'),
    path('api/job-posts/create/', views.api_job_post_create, name='api_job_post_create'),
    path('api/job-posts/<int:pk>/', views.api_job_post_detail, name='api_job_post_detail'),
    path('api/job-posts/<int:pk>/update/', views.api_job_post_update, name='api_job_post_update'),
    path('api/job-posts/<int:pk>/delete/', views.api_job_post_delete, name='api_job_post_delete'),
    # API: Proposals
    path('api/job-posts/<int:job_post_id>/proposals/', views.api_proposal_submit, name='api_proposal_submit'),
    path('api/job-posts/<int:job_post_id>/proposals/<int:proposal_id>/accept/', views.api_proposal_accept, name='api_proposal_accept'),
]
