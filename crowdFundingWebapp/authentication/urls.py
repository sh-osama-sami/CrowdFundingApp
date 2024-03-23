from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'), 
    path('verify/<int:user_id>/', views.verify_email, name='verify'),
    path('admin/', views.admin_login, name='administration'),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('login/', views.signin, name='login'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('profile/delete/<int:user_id>/', views.delete_account, name='delete_account'),

]

