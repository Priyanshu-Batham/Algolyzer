import os

from celery import shared_task
from django.conf import settings
from django.utils.timezone import now
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
            "distilbert-base-uncased-finetuned-sst-2-english",
        )

        # Load model from saved directory
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        sentiment_pipeline = pipeline(
            "sentiment-analysis", model=model, tokenizer=tokenizer
        )

        if not model:
            raise ValueError(
                "Model 'distilbert-base-uncased-finetuned-sst-2-english' not found."
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
