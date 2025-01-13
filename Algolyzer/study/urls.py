from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page_view, name="landing_page"),
    path("topic/<int:topic_id>/", views.topic_detail_view, name="topic_detail"),
]
