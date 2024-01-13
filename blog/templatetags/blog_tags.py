from django import template
from blog.models import Post

register = template.Library()


@register.simple_tag()
def total_post():
    return Post.objects.filter(status=Post.Status.PUBLISHED).count()


@register.inclusion_tag(filename='blog/latest_post.html')
def show_latest_post(count=5):
    latest_post = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('dt_publish')[:count]
    return {'latest_post': latest_post}
