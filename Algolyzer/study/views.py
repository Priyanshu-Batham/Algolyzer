from django.shortcuts import render


def home(request):
    return render(request, "study/home.html")


def sentiment_analysis(request):
    return render(request, "study/sentiment_analysis.html")


def doodle_classifier(request):
    return render(request, "study/doodle_classifier.html")


def linear_regression(request):
    return render(request, "study/linear_regression.html")


def k_means_clustering(request):
    return render(request, "study/k_means_clustering.html")


def svm_regression(request):
    return render(request, "study/svm_regression.html")
