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
    # path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('search_helper/', search_helper, name='search_helper'),
    path('project_list/', project_list, name='project_list'),
    path('update_featured_status/<int:project_id>/', update_featured_status, name='update_featured_status'),
    path('project/<int:pk>/', project_details, name='project_details'),
    path('report/<int:pk>/', report_project, name='report_project'),
    path('report_comment/<int:comment_id>/', report_comment, name='report_comment'),
    path('donate/<int:pk>/', donate, name='donate'),
    path('projects/<int:project_id>/rate/',rate_project, name='rate_project'),
    path('report_details_admin/<int:project_id>', report_details_admin, name="report_details_admin"),
    path('admin_suspend_project/<int:project_id>', admin_suspend_project, name="admin_suspend_project"),
    path('admin_delete_project/<int:project_id>', admin_delete_project, name="admin_delete_project"),
    path('admin_ignore_reports/<int:project_id>', admin_ignore_reports, name="admin_ignore_reports"),

]
