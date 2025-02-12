from django.contrib import admin

from .models import PlaygroundTask


@admin.register(PlaygroundTask)
class PlaygroundTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "model_name", "status", "created_at", "completed_at")
    list_filter = ("status", "model_name", "created_at")
    search_fields = ("user__username", "celery_task_id", "model_name", "input_data")
    readonly_fields = ("created_at", "completed_at", "celery_task_id")
