from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from home.decorators import profile_required


@login_required
@profile_required
def quiz_home(request):
    """Main QUIZ Home Page"""
    return render(request, "quiz/quiz_home.html")
