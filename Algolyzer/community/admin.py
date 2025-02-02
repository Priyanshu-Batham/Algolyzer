from django.contrib import admin

from .models import Category, Comment, Post, Vote

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Category)
