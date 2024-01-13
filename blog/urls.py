from django.urls import path

from blog.views import post_list, post_detail, post_share, post_comment, post_search
from blog.feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/share', post_share, name='post_share'),
    path('post/<int:post_id>/comment', post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('post/search', post_search, name='post_search'),
]
