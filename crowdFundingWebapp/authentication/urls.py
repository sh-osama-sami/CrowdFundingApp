from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('verify/<int:user_id>/', views.verify_email, name='verify'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
