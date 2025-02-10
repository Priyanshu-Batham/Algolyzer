import os

from celery import Celery

# Use the existing DJANGO_SETTINGS_MODULE if it's already set, otherwise set a default
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "Algolyzer.settings.development"),
)

celery_app = Celery("Algolyzer")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
celery_app.autodiscover_tasks()
