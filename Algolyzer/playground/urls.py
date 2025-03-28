from django.urls import path

from .views import doodle_classifier, playground_home, sentiment_analysis

urlpatterns = [
    path("", playground_home, name="playground_home"),
    path("sentiment_analysis/", sentiment_analysis, name="sentiment_analysis"),
    path("doodle_classifier/", doodle_classifier, name="doodle_classifier"),
]
