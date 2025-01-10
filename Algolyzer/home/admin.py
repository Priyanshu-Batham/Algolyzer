from django.contrib import admin

from .models import UserProfile


# Optionally, create a custom admin class to manage the model
class UserProfileAdmin(admin.ModelAdmin):
    # Define fields to display in the list view
    list_display = ("user", "dob", "xp", "level")
    # Optionally, allow searching by the user's username
    search_fields = ("user__username",)


# Register the UserProfile model with the admin
admin.site.register(UserProfile, UserProfileAdmin)
