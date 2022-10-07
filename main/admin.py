from django.contrib import admin
from .models import Category, Post, Comment, PostImage
# Register your models here.

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Category)
admin.site.register(Comment)
