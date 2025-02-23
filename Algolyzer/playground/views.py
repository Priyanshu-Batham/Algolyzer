import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from home.decorators import profile_required
from playground.tasks import sentiment_analysis_task

from django.core.files.base import ContentFile
import base64
import io
import os
from PIL import Image
import numpy as np
from playground.tasks import doodle_classifier_task

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



# @login_required
# @profile_required
# def doodle_classifier(request):
#     """Handles doodle classification model submission and task status retrieval."""
#     user = request.user

#     if request.method == "POST":
#         # Get the base64 image data from the form
#         image_data = request.POST.get("image_data")
#         format, imgstr = image_data.split(';base64,')
#         ext = format.split('/')[-1]
#         image_file = ContentFile(base64.b64decode(imgstr), name=f'doodle.{ext}')

#         # Create a task entry in the database
#         task = PlaygroundTask.objects.create(
#             user=user,
#             input_image=image_file,
#             model_name="doodle_classifier",
#             status="PENDING",
#         )

#         # Call Celery and attach the Celery task ID to the database entry
#         celery_task = doodle_classifier_task.apply_async(args=[task.id])
#         task.celery_task_id = celery_task.id
#         task.save()

#         return redirect("doodle_classifier")

#     else:
#         """Handles task status retrieval."""
#         previous_results = PlaygroundTask.objects.filter(
#             user=user, model_name="doodle_classifier"
#         ).order_by("-created_at")

#         context = {"previous_results": previous_results}
#         return render(request, "playground/doodle_classifier.html", context=context)

@login_required
@profile_required
def doodle_classifier(request):
    """Handles doodle classification model submission and task status retrieval."""
    user = request.user

    if request.method == "POST":
        image_data = request.POST.get("image_data")

        if not image_data:
            return JsonResponse({"error": "No image data received"}, status=400)

        # Extract base64 part (remove `data:image/png;base64,`)
        try:
            image_data = image_data.split(",")[1]  # <- This is where the error was happening
        except (AttributeError, IndexError):
            return JsonResponse({"error": "Invalid image format"}, status=400)

        # Save task in DB
        task = PlaygroundTask.objects.create(
            user=user,
            input_data="Doodle Image",  # Placeholder
            model_name="doodle_classifier",
            status="PENDING",
        )

        # Call Celery task
        celery_task = doodle_classifier_task.apply_async(args=[task.id, image_data])
        task.celery_task_id = celery_task.id
        task.save()

        return JsonResponse({"message": "Task submitted successfully", "task_id": task.id})

    else:
        previous_results = PlaygroundTask.objects.filter(
            user=user, model_name="doodle_classifier"
        ).order_by("-created_at")

        context = {"previous_results": previous_results}
        return render(request, "playground/doodle_classifier.html", context)
