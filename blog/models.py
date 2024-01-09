from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Публиковать'

    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='слаг')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='автор')
    content = models.TextField(blank=True, verbose_name='контент')
    dt_created = models.DateTimeField(default=timezone.now, verbose_name='дата создания')
    dt_publish = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='статус')

    objects = models.Manager()

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-dt_publish']
        indexes = [
            models.Index(fields=['-dt_publish'])
        ]

    def get_absolute_url(self):
        return reverse(viewname='blog:post_detail', args=[self.id])

    def __str__(self):
        return self.title
