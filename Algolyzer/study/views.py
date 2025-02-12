from django.shortcuts import render


def home(request):
    return render(request, "study/home.html")


def sentiment_analysis(request):
    return render(request, "study/sentiment_analysis.html")
