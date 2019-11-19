from django.contrib import admin
from .models import Post, Comment, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)

