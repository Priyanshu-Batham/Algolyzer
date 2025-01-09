from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    """Main Home Page"""
    return render(request, "home/home.html")


@login_required
def dashboard(request):
    """Dashboard page for logged in users only"""
    return render(request, "home/dashboard.html")
