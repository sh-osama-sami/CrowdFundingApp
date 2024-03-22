from django.urls import path
from .views import *

urlpatterns = [
    path('create_category/', create_category, name='create_category'),
    path('select_featured_projects', select_featured_projects , name = 'select_featured_projects'),
    path('create/', create_project, name='create_project'),
    path('<int:project_id>/', project_detail, name='project_detail'),
    path('<int:project_id>/update/', update_project, name='update_project'),
    path('<int:project_id>/delete/', delete_project, name='delete_project'),
    path('user_projects/', user_projects, name='user_projects'),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('project_list/', project_list, name='project_list'),
    path('update_featured_status/<int:project_id>/', update_featured_status, name='update_featured_status')

]
