from django.contrib import admin

from .models import Question, QuizProgress, Topic, UserAnswer


# Customize admin interface for Topic
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # Display the ID and name of topics
    search_fields = ("name",)  # Enable search by name


# Customize admin interface for Question
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "text", "correct_answer")  # Show key details
    list_filter = ("topic",)  # Add a filter by topic
    search_fields = ("text",)  # Enable search by question text


# Customize admin interface for UserAnswer
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "question",
        "selected_answer",
        "is_correct",
    )  # Show key details
    list_filter = ("is_correct",)  # Filter by correctness
    search_fields = (
        "user__username",
        "question__text",
    )  # Enable search by user or question


# Customize admin interface for QuizProgress
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "topic",
        "current_question",
        "completed",
    )  # Show progress details
    list_filter = ("completed",)  # Filter by completion status
    search_fields = ("user__username", "topic__name")  # Enable search by user or topic


# Register models with their respective ModelAdmin
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(QuizProgress, QuizProgressAdmin)
