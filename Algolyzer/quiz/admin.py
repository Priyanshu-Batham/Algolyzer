from django.contrib import admin

from .models import Question, QuizProgress, Topic, UserAnswer


# Inline for Questions
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display


# Customize admin interface for Topic
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "difficulty")
    search_fields = ("name",)
    list_filter = ("difficulty",)
    inlines = [QuestionInline]


# Customize admin interface for Question
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "text", "correct_answer")
    list_filter = ("topic", "topic__difficulty")
    search_fields = ("text",)
    fieldsets = (
        (None, {"fields": ("topic", "text")}),
        ("Options", {"fields": ("option_a", "option_b", "option_c", "option_d")}),
        ("Correct Answer", {"fields": ("correct_answer",)}),
    )
    radio_fields = {
        "correct_answer": admin.HORIZONTAL
    }  # Use radio buttons for correct_answer


# Customize admin interface for UserAnswer
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "selected_answer", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("user__username", "question__text")
    readonly_fields = ("is_correct",)  # Make is_correct read-only


# Customize admin interface for QuizProgress
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "current_question", "completed")
    list_filter = ("completed",)
    search_fields = ("user__username", "topic__name")
    actions = ["mark_as_completed"]

    def mark_as_completed(self, request, queryset):
        queryset.update(completed=True)

    mark_as_completed.short_description = "Mark selected progress records as completed"


# Register models with their respective ModelAdmin
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(QuizProgress, QuizProgressAdmin)
