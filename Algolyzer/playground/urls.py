from django.urls import path

from .views import doodle_classifier, playground_home, sentiment_analysis, task_status

urlpatterns = [
    path("", playground_home, name="playground_home"),
    path("sentiment_analysis/", sentiment_analysis, name="sentiment_analysis"),
    path("doodle_classifier/", doodle_classifier, name="doodle_classifier"),
    path("task/<str:task_id>/", task_status, name="task_status"),
]
