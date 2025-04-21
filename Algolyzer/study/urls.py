from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="study_home"),
    path(
        "sentiment_analysis/", views.sentiment_analysis, name="sentiment_analysis_study"
    ),
    path("doodle_classifer/", views.doodle_classifier, name="doodle_classifier_study"),
    path("linear_regression/", views.linear_regression, name="linear_regression_study"),
    path("k_means_clustering/", views.k_means_clustering, name="k_means_clustering"),
    path("svm_regression/", views.svm_regression, name="svm_regression"),
]
