import base64
import json
import os

import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from django.utils.timezone import now
from home.decorators import profile_required
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

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

        # Call Celery and attach the Celery task ID to the database entry
        try:
            MODEL_DIR = os.path.join(
                settings.BASE_DIR,
                "playground",
                "aiml_models",
                "finiteautomata_bertweet-base-sentiment-analysis",
            )

            # Load model from saved directory
            tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
            sentiment_pipeline = pipeline(
                "sentiment-analysis", model=model, tokenizer=tokenizer
            )

            if not model:
                raise ValueError(
                    "Model 'finiteautomata_bertweet-base-sentiment-analysis' not found."
                )

            # Process the input with the model
            result = sentiment_pipeline(input_data)[0]

            # Create a task entry in the database
            task = PlaygroundTask.objects.create(
                user=user,
                input_data=input_data,
                model_name="sentiment_analysis",
                result=str(result),
                completed_at=now(),
                status="COMPLETED",
            )

            task.save()

        except Exception as e:
            task.status = "FAILED"
            task.result = str(e)
            task.save()
            # raise e
        task.save()

        return redirect("sentiment_analysis")

    else:
        """Handles task status retrieval."""

        previous_results = PlaygroundTask.objects.filter(
            user=user, model_name="sentiment_analysis"
        ).order_by("-created_at")

        for task in previous_results:
            try:
                # Replace single quotes with double quotes to make it valid JSON
                formatted_result = task.result.replace("'", '"')
                task.result = json.loads(formatted_result)
            except json.JSONDecodeError:
                task.result = {}  # If JSON is invalid, set it as an empty dictionary
        context = {"previous_results": previous_results}
        return render(request, "playground/sentiment_analysis.html", context=context)


# Load the pre-trained MNIST model from Hugging Face
mnist_classifier = pipeline(
    "image-classification", model="farleyknight/mnist-digit-classification-2022-09-04"
)


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
        )

        # Save the image file to the task's input_image field
        task.input_image.save(f"doodle_{task.id}.png", image_file)
        task.save()

        # Call Celery task
        try:
            # Open the saved PNG image from the input_image field
            image = Image.open(task.input_image.path)
            print("image being loaded: ", image.filename)

            # Run inference using the pre-trained model
            result = mnist_classifier(image)
            print(str(result))
            best_prediction = max(result, key=lambda x: x["score"])
            best_label = best_prediction["label"]
            # print("Label: ", best_label, "Score: ", best_score)

            # Update the task with the result
            task.result = best_label  # Convert the result to a string for storage
            task.status = "COMPLETED"
            task.save()

        except Exception as e:
            # Handle any errors that occur during processing
            task.result = str(e)  # Store the error message
            task.status = "FAILED"
        task.save()

        return redirect("doodle_classifier")

    else:
        # Fetch previous results
        previous_results = PlaygroundTask.objects.filter(
            user=user, model_name="doodle_classifier"
        ).order_by("-created_at")

        context = {"previous_results": previous_results}
        return render(request, "playground/doodle_classifier.html", context=context)


@login_required
def linear_regression(request):
    if request.method == "POST":
        # Collect form data (values from 5 sliders)
        values = [
            float(request.POST.get("value_1", 0)),
            float(request.POST.get("value_2", 0)),
            float(request.POST.get("value_3", 0)),
            float(request.POST.get("value_4", 0)),
            float(request.POST.get("value_5", 0)),
        ]

        # Prepare data for linear regression
        X = np.array(range(1, 6)).reshape(-1, 1)  # Indices 1 to 5
        y = np.array(values)  # Slider values

        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the next value (for index 6)
        next_index = np.array([[6]])
        predicted_value = model.predict(next_index)[0]

        # Get regression line parameters for plotting
        slope = model.coef_[0]
        intercept = model.intercept_

        # Pass data to template
        return render(
            request,
            "playground/linear_regression.html",
            {
                "predicted_value": round(predicted_value, 2),
                "input_values": values,
                "slope": slope,
                "intercept": intercept,
                "show_chart": True,  # Flag to display chart
            },
        )

    else:
        return render(request, "playground/linear_regression.html")


@login_required
def kmeans_clustering(request):
    if request.method == "POST":
        # Collect form data
        values_json = request.POST.get("values", "[]")
        try:
            input_values = json.loads(values_json)
            if not input_values:
                raise ValueError("No values provided")

            # Convert input values to numpy array for K-Means
            X = np.array(input_values).reshape(-1, 1)  # Reshape for single feature

            # Apply K-Means clustering
            n_clusters = min(len(input_values), 3)  # Limit to 3 clusters or fewer
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(X)

            # Get cluster labels
            labels = kmeans.labels_.tolist()

            # Prepare classified values (pair each value with its cluster)
            classified_values = list(zip(input_values, labels))

            # Prepare data for Chart.js
            chart_data = {
                "values": input_values,
                "labels": labels,
                "clusters": [
                    {"x": float(val), "cluster": int(label)}
                    for val, label in classified_values
                ],
            }

            # Pass data to template
            return render(
                request,
                "playground/kmeans_clustering.html",
                {
                    "input_values": input_values,
                    "classified_values": classified_values,
                    "show_chart": True,
                    "chart_data": json.dumps(chart_data),  # Serialize for JavaScript
                },
            )

        except (json.JSONDecodeError, ValueError):
            # Handle invalid input
            return render(
                request,
                "playground/kmeans_clustering.html",
                {"error": "Please enter valid numbers."},
            )

    else:
        return render(request, "playground/kmeans_clustering.html")
