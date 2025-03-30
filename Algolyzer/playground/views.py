import base64
import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from home.decorators import profile_required
from playground.tasks import doodle_classifier_task, sentiment_analysis_task

from .models import PlaygroundTask


@login_required
@profile_required
# Home Page
def playground_home(request):
    """Renders the playground home page."""
    return render(request, "playground/home.html")


@login_required
@profile_required
# Sentiment Analysis
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

        return redirect("task_status", task_id=celery_task.id)

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


@login_required
def doodle_classifier(request):
    user = request.user

    if request.method == "POST":
        # Get the base64 image data from the form
        image_data = request.POST.get("image_data")
        format, imgstr = image_data.split(";base64,")
        ext = format.split("/")[-1]

        # Decode the base64 image and save it as a PNG file
        image_file = ContentFile(base64.b64decode(imgstr), name=f"doodle.{ext}")

        # Create a task entry in the database
        task = PlaygroundTask.objects.create(
            user=user,
            input_data=image_data,  # Store the base64 data for reference
            model_name="doodle_classifier",
            status="PENDING",
        )

        # Save the image file to the task's input_image field
        task.input_image.save(f"doodle_{task.id}.png", image_file)
        task.save()

        # Call Celery task
        celery_task = doodle_classifier_task.apply_async(args=[task.id])
        task.celery_task_id = celery_task.id
        task.save()

        return redirect("task_status", task_id=celery_task.id)

    else:
        # Fetch previous results
        previous_results = PlaygroundTask.objects.filter(
            user=user, model_name="doodle_classifier"
        ).order_by("-created_at")

        context = {"previous_results": previous_results}
        return render(request, "playground/doodle_classifier.html", context=context)


@login_required
@profile_required
def task_status(request, task_id):
    """View to check task status and show progress."""
    try:
        task = PlaygroundTask.objects.get(celery_task_id=task_id, user=request.user)

        # Calculate progress value based on status
        if task.status == "COMPLETED":
            progress_value = 100
        elif task.status == "PROCESSING":
            # Calculate progress based on time elapsed since creation
            from datetime import datetime, timezone

            now = datetime.now(timezone.utc)
            elapsed = (now - task.created_at).total_seconds()
            # Assuming average processing time is 30 seconds
            progress_value = min(int((elapsed / 30) * 95), 95)
        elif task.status == "FAILED":
            progress_value = 0
        else:  # PENDING
            progress_value = 0

        context = {
            "task_id": task_id,
            "status": task.status,
            "result": task.result,
            "progress_value": progress_value,
        }
        return render(request, "playground/task_status.html", context=context)
    except PlaygroundTask.DoesNotExist:
        context = {"error": "Task not found"}
        return render(request, "playground/task_status.html", context=context)
