from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('verify/<int:user_id>/', views.verify_email, name='verify'),
    path('admin/', views.admin_login, name='administration'),
    path('admin/home/', views.admin_home, name='admin_home'),
]
