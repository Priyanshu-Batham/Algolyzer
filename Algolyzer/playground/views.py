import json

from django.shortcuts import redirect, render
from playground.tasks import sentiment_analysis_task

from .models import PlaygroundTask


# Home Page
def playground_home(request):
    """Renders the playground home page."""
    return render(request, "playground/home.html")


# Task Submission View


def sentiment_analysis(request):
    """Handles sentiment analysis model submission and task status retrieval."""
    user = request.user  # Ensure the user is authenticated

    if request.method == "POST":
        input_data = request.POST.get("input_data")

        # Create a task entry in the database
        task = PlaygroundTask.objects.create(
            user=user,
            input_data=input_data,
            model_name="sentiment_analysis",
            status="PENDING",
        )

        # Call Celery and attach the Celery task ID to the database entry
        celery_task = sentiment_analysis_task.apply_async(args=[task.id, input_data])
        task.celery_task_id = celery_task.id
        task.save()

        return redirect("sentiment_analysis")

    else:
        """Handles task status retrieval."""

        previous_results = PlaygroundTask.objects.filter(
            user=user, model_name="sentiment_analysis"
        ).order_by("-created_at")

        for task in previous_results:
            if task.result:
                try:
                    # Replace single quotes with double quotes to make it valid JSON
                    formatted_result = task.result.replace("'", '"')
                    task.result = json.loads(formatted_result)
                except json.JSONDecodeError:
                    task.result = (
                        {}
                    )  # If JSON is invalid, set it as an empty dictionary
        context = {"previous_results": previous_results}
        return render(request, "playground/sentiment_analysis.html", context=context)
