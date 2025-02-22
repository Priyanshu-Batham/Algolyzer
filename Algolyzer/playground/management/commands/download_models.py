import os

from django.core.management.base import BaseCommand
from transformers import AutoModel, AutoTokenizer

# Define models to download
MODELS = {
    "sentiment-analysis": "finiteautomata/bertweet-base-sentiment-analysis",
}

# Define directory for saving models
MODEL_DIR = os.path.join("playground", "aiml_models")


class Command(BaseCommand):
    help = "Download Hugging Face models for use in Django views"

    def handle(self, *args, **kwargs):
        os.makedirs(MODEL_DIR, exist_ok=True)
        for task, model_name in MODELS.items():
            self.stdout.write(
                self.style.SUCCESS(f"Downloading {task} model: {model_name}...")
            )

            # Download model and tokenizer
            model = AutoModel.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Save them in the specified directory
            model.save_pretrained(os.path.join(MODEL_DIR, model_name.replace("/", "_")))
            tokenizer.save_pretrained(
                os.path.join(MODEL_DIR, model_name.replace("/", "_"))
            )

            self.stdout.write(
                self.style.SUCCESS(f"✔ Model {model_name} downloaded successfully!\n")
            )
