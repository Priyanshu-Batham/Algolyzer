from django.urls import path

from .views import dashboard, home, level_up, onboarding

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("onboarding/", onboarding, name="onboarding"),
    # level_up route is temporary only for dev testing
    path("level_up/", level_up, name="level_up"),
]
