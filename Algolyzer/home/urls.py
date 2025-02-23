from django.urls import path

from .views import dashboard, home, onboarding

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("onboarding/", onboarding, name="onboarding"),
]
