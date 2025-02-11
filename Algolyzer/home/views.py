from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import OnboardingForm
from .models import UserProfile


def home(request):
    """Main Home Page"""
    return render(request, "home/home.html")


@login_required
def dashboard(request):
    """Dashboard page for logged in users only"""
    context = {"user_profile": UserProfile.objects.filter(user=request.user).first()}
    return render(request, "home/dashboard.html", context=context)


@login_required
def onboarding(request):
    # Check if the UserProfile exists
    if UserProfile.objects.filter(user=request.user).exists():
        return redirect("dashboard")  # Redirect if profile exists

    if request.method == "POST":
        # If the profile doesn't exist, no instance is passed to the form
        form = OnboardingForm(request.POST)

        if form.is_valid():
            # Create the UserProfile only after form validation
            UserProfile.objects.create(user=request.user, dob=form.cleaned_data["dob"])
            return redirect("dashboard")
    else:
        # On GET request, just create an empty form (no instance)
        form = OnboardingForm()

    return render(request, "home/onboarding.html", {"form": form})


# level_up view is temporary only for dev testing
@login_required
def level_up(request):
    if UserProfile.objects.filter(user=request.user).exists():
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.add_xp(100)
        return redirect("dashboard")
