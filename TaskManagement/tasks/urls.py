from django.urls import path
from .views import *

urlpatterns = [
    path('get_tasks_details', get_all_tasks),
    path('create_new_task', create_new_task),
    path('delete_task', delete_task),
    path('update_task_status', update_task_status),
    path('get_project_details', get_all_projects),
    path('create_new_project', create_new_project),
    path('delete_project', delete_project),
    path('get_project_detail', get_project_detail),
]