import os

from celery import shared_task
from django.conf import settings
from django.utils.timezone import now
from PIL import Image
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from .models import PlaygroundTask


@shared_task(bind=True)
def sentiment_analysis_task(self, task_db_id, input_data):
    """Celery task to process ML model input."""
    try:
        # Fetch the task from the database
        task = PlaygroundTask.objects.get(id=task_db_id)
        task.status = "PROCESSING"
        task.save()

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

        # Update the task in the database
        task.status = "COMPLETED"
        task.result = str(result)  # Convert to JSON-friendly format if needed
        task.completed_at = now()
        task.save()

    except Exception as e:
        task.status = "FAILED"
        task.result = str(e)
        task.save()
        # raise e

    return task.result  # Celery stores the result


# Load the pre-trained MNIST model from Hugging Face
mnist_classifier = pipeline(
    "image-classification", model="farleyknight/mnist-digit-classification-2022-09-04"
)


@shared_task
def doodle_classifier_task(task_id):
    try:
        # Get the task
        task = PlaygroundTask.objects.get(id=task_id)

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
        task = PlaygroundTask.objects.get(id=task_id)
        task.result = str(e)  # Store the error message
        task.status = "FAILED"
        task.save()

    return task.result
