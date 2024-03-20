from django.urls import path, include
from . import views
from Project import views as pviews
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('admin/', views.admin_login, name='administration'),
    path('admin/home/', views.admin_home, name='admin_home'),
]
