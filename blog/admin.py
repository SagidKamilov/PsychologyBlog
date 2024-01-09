from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'dt_publish']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
