from django.shortcuts import redirect, render
from playground.tasks import process_ml_task

from .models import PlaygroundTask


# Home Page
def playground_home(request):
    """Renders the playground home page."""
    return render(request, "playground/home.html")


# Task Submission View
def submit_task_view(request):
    """Handles ML model submission through a form."""
    if request.method == "POST":
        user = request.user  # Ensure the user is authenticated
        input_data = request.POST.get("input_data")
        model_name = request.POST.get("model_name", "model_1")  # Default to model_1

        if model_name not in ["model_1", "model_2"]:  # Validate model selection
            return render(
                request, "playground/home.html", {"error": "Invalid model selected"}
            )

        # Create a task entry in the database
        task = PlaygroundTask.objects.create(
            user=user,
            model_name=model_name,
            input_data=input_data,
            status="PENDING",
        )

        # Call Celery and attach the Celery task ID to the database entry
        celery_task = process_ml_task.apply_async(
            args=[task.id, model_name, input_data]
        )
        task.celery_task_id = celery_task.id
        task.save()

        return redirect("task_status_view", task_id=task.celery_task_id)

    return render(request, "playground/home.html")


# Task Status View
def check_task_status_view(request, task_id):
    """Renders the task status page."""
    try:
        task = PlaygroundTask.objects.get(celery_task_id=task_id)
        context = {
            "task_id": task.celery_task_id,
            "status": task.status,
            "result": task.result if task.status == "COMPLETED" else None,
        }
        return render(request, "playground/task_status.html", context)
    except PlaygroundTask.DoesNotExist:
        return render(
            request, "playground/task_status.html", {"error": "Task not found"}
        )
