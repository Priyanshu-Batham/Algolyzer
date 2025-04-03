from django.contrib.auth.models import User
from django.db import models


class PlaygroundTask(models.Model):
    STATUS_CHOICES = [
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)  # Selected ML model
    input_data = models.TextField()  # Store user input (can be JSON)
    input_image = models.ImageField(upload_to="doodles/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    result = models.TextField(blank=True, null=True)  # ML output
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Task {self.model_name} - {self.status}"
