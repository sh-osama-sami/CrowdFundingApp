from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'), 
    path('verify/<int:user_id>/<str:token>/', views.verify_email, name='verify'),
    path('resend_verification_email/<str:username>/', views.resend_verification_email, name='resend_verification_email'),
    path('admin/', views.admin_login, name='administration'),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('profile/delete/<int:user_id>/', views.delete_account, name='delete_account'),
    path('Project/error/', views.error_page, name='error_page'),
    path('', include('django.contrib.auth.urls')),
]

