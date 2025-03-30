from community.models import Comment, Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from playground.models import PlaygroundTask
from quiz.models import QuizProgress, Topic

from .forms import OnboardingForm
from .models import UserProfile


def home(request):
    """Main Home Page"""
    return render(request, "home/home.html")


@login_required
def dashboard(request):
    """Dashboard page for logged-in users only"""
    # Fetch the user's profile
    user_profile = UserProfile.objects.filter(user=request.user).first()

    # Redirect to onboarding if no profile exists
    if not user_profile:
        return redirect("onboarding")

    # Calculate XP progress percentage
    next_level_xp = user_profile.get_next_level_xp()
    progress_percentage = (
        (user_profile.xp / next_level_xp) * 100 if next_level_xp else 0
    )

    # Fetch quiz progress data
    completed_quizzes = QuizProgress.objects.filter(
        user=request.user, completed=True
    ).count()
    total_quizzes = Topic.objects.count()
    recent_quizzes = QuizProgress.objects.filter(
        user=request.user, completed=True
    ).order_by("-id")[:5]

    # Fetch task data
    completed_tasks = PlaygroundTask.objects.filter(
        user=request.user, status="COMPLETED"
    ).count()
    pending_tasks = PlaygroundTask.objects.filter(
        user=request.user, status="PENDING"
    ).count()
    recent_tasks = PlaygroundTask.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]

    # Fetch forum activity data
    total_posts = Post.objects.filter(author=request.user).count()
    total_comments = Comment.objects.filter(author=request.user).count()
    recent_posts = Post.objects.filter(author=request.user).order_by("-created_at")[:5]
    recent_comments = Comment.objects.filter(author=request.user).order_by(
        "-created_at"
    )[:5]

    # Prepare context
    context = {
        "user_profile": user_profile,
        "progress_percentage": progress_percentage,  # XP progress percentage
        "completed_quizzes": completed_quizzes,  # Number of completed quizzes
        "total_quizzes": total_quizzes,  # Total number of quizzes
        "recent_quizzes": recent_quizzes,  # Recent quizzes
        "completed_tasks": completed_tasks,  # Number of completed tasks
        "pending_tasks": pending_tasks,  # Number of pending tasks
        "recent_tasks": recent_tasks,  # Recent tasks
        "total_posts": total_posts,  # Total number of posts
        "total_comments": total_comments,  # Total number of comments
        "recent_posts": recent_posts,  # Recent posts
        "recent_comments": recent_comments,  # Recent comments
    }

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
