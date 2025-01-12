from django.urls import path

from .views import quiz_home

urlpatterns = [
    path("", quiz_home, name="quiz_home"),
]
