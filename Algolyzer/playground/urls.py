from django.urls import path

from .views import check_task_status_view, playground_home, submit_task_view

urlpatterns = [
    path("", playground_home, name="playground_home"),
    path("submit_task/", submit_task_view, name="submit_task_view"),
    path("task_status/<str:task_id>/", check_task_status_view, name="task_status_view"),
]
