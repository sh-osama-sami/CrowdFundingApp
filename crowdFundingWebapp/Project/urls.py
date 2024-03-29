from django.urls import path
from .views import *
from authentication.views import admin_home

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
    path('all_categories/', all_categories, name='all_categories'),
    path('category/<int:category_id>/', category_projects, name='category_projects'),
    path('projects/<int:project_id>/rate/',rate_project, name='rate_project'),
    path('report_details_admin/<int:project_id>', report_details_admin, name="report_details_admin"),
    path('admin_suspend_project/<int:project_id>', admin_suspend_project, name="admin_suspend_project"),
    path('admin_delete_project/<int:project_id>', admin_delete_project, name="admin_delete_project"),
    path('admin_ignore_reports/<int:project_id>', admin_ignore_reports, name="admin_ignore_reports"),
    path('admin/home/', admin_home, name='admin_home'),
    path('admin_project_details/<int:project_id>', admin_project_details, name="admin_project_details"),
    path('error/', error_page, name='error_page'),
    path('reply_comment/<int:parent_id>/', reply_comment, name='reply_comment'),
    path('categoryDetails/<int:category_id>/', categoryDetails, name='categoryDetails'),


]
