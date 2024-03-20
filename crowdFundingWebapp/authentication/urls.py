from django.urls import path, include
from authentication.views import register

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),

]
