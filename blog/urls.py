from django.urls import path
from .views import post_list, post_detail

app_name = 'blog'

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
