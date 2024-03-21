from django.urls import path
from .views import *

urlpatterns = [
    path('create_category/', create_category, name='create_category'),
    path('select_featured_projects', select_featured_projects , name = 'select_featured_projects'),
]
