from django.urls import path

from .views import (
    doodle_classifier,
    kmeans_clustering,
    linear_regression,
    playground_home,
    sentiment_analysis,
    svm_regression,
)

urlpatterns = [
    path("", playground_home, name="playground_home"),
    path("linear_regression", linear_regression, name="linear_regression"),
    path("kmeans_clustering", kmeans_clustering, name="kmeans_clustering"),
    path("svm_regression", svm_regression, name="svm_regression"),
    path("sentiment_analysis/", sentiment_analysis, name="sentiment_analysis"),
    path("doodle_classifier/", doodle_classifier, name="doodle_classifier"),
]
