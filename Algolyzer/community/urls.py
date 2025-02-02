from django.urls import path

from . import views

urlpatterns = [
    path("", views.category_list, name="category_list"),
    path(
        "category/<int:category_id>/",
        views.post_list_by_category,
        name="post_list_by_category",
    ),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/vote/<str:vote_type>/", views.vote_post, name="vote_post"),
]
