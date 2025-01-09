from django.urls import path

from .views import dashboard, home

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
]
