from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="study_home"),
    path(
        "sentiment_analysis/", views.sentiment_analysis, name="sentiment_analysis_study"
    ),
]
