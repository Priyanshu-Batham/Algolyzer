from django.contrib import admin

from .models import Category, Topic


# Register Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")  # Columns to display in the admin list view
    search_fields = ("name",)  # Add a search bar to search categories by name


admin.site.register(Category, CategoryAdmin)


# Register Module model
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "created_at",
    )  # Display title, category, and creation date in admin
    search_fields = ("title",)  # Add a search bar to search modules by title
    list_filter = ("category",)  # Filter modules by category


admin.site.register(Topic, TopicAdmin)
