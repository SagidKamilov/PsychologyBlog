from django.urls import path
from .views import PostListView, PostDetailView, post_share

app_name = 'blog'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/share', post_share, name='post_share'),
]
