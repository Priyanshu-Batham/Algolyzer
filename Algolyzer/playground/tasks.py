import os
import io
import base64
import numpy as np
from PIL import Image

from celery import shared_task
from django.conf import settings
from django.utils.timezone import now
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch
import torchvision.transforms as transforms
from torchvision import models


from django.utils.timezone import now
import tensorflow as tf

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



# @shared_task(bind=True)
# def doodle_classifier_task(self, task_db_id):
#     try:
#         # Fetch the task from the database
#         task = PlaygroundTask.objects.get(id=task_db_id)
#         task.status = "PROCESSING"
#         task.save()

#         # Load the pre-trained model
#         model = tf.keras.applications.MobileNetV2(weights='imagenet')
#         model = tf.keras.Model(inputs=model.input, outputs=model.layers[-2].output)

#         # Load and preprocess the image
#         img = Image.open(task.input_image.path)

#         # Convert RGBA to RGB if the image has 4 channels
#         if img.mode == 'RGBA':
#             img = img.convert('RGB')

#         # Resize the image to the required input size
#         img = img.resize((224, 224))

#         # Convert the image to a numpy array
#         img_array = tf.keras.preprocessing.image.img_to_array(img)

#         # Add batch dimension
#         img_array = tf.expand_dims(img_array, axis=0)

#         # Preprocess the image for MobileNetV2
#         img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

#         # Log the shape of the input array
#         print("Image shape after preprocessing:", img_array.shape)

#         # Predict the class
#         predictions = model.predict(img_array)
#         predicted_class = np.argmax(predictions, axis=1)

#         # Update the task in the database
#         task.status = "COMPLETED"
#         task.result = {"class": int(predicted_class), "confidence": float(np.max(predictions))}
#         task.completed_at = now()
#         task.save()

#     except Exception as e:
#         task.status = "FAILED"
#         task.result = {"error": str(e)}
#         task.save()
#         print(f"Error in doodle_classifier_task: {e}")

#     return task.result


@shared_task(bind=True)
def doodle_classifier_task(self, task_db_id, image_data):
    """Celery task to classify doodle images."""
    try:
        # Fetch the task from the database
        task = PlaygroundTask.objects.get(id=task_db_id)
        task.status = "PROCESSING"
        task.save()

        # Decode the Base64 image
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Define image transformations
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=3),  # Convert to 3-channel grayscale
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

        image = transform(image).unsqueeze(0)  # Add batch dimension

        # Load a lightweight pretrained model
        model = models.mobilenet_v2(pretrained=True)
        model.classifier[1] = torch.nn.Linear(model.last_channel, 4)  # Adjust for 4 categories
        model.eval()

        # Dummy labels for 4 categories
        categories = ["Circle", "Square", "Triangle", "Star"]

        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            result = categories[predicted.item()]

        # Update the task in the database
        task.status = "COMPLETED"
        task.result = result
        task.completed_at = now()
        task.save()

    except Exception as e:
        task.status = "FAILED"
        task.result = str(e)
        task.save()
        # raise e

    return task.result  # Celery stores the result
