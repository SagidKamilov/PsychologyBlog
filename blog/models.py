from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField(blank=True)
    dt_created = models.DateTimeField(default=timezone.now)
    dt_publish = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-dt_publish']
        indexes = [
            models.Index(fields=['-dt_publish'])
        ]

    def __str__(self):
        return self.title
