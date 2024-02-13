from django.urls import path
from email_service import views

urlpatterns = [
    path('', views.health, name='health'),
    path('health', views.health, name='health2'),
    path('email', views.post_email, name='email'),
]
