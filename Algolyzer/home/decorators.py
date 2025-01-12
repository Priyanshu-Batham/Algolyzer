from functools import wraps

from django.shortcuts import redirect
from home.models import UserProfile


def profile_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not UserProfile.objects.filter(user=request.user).exists():
            return redirect("onboarding")  # Replace with your onboarding route name
        return view_func(request, *args, **kwargs)

    return _wrapped_view
