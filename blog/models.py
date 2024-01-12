from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Публиковать'

    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.SlugField(max_length=255, unique_for_date='dt_publish', verbose_name='слаг')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='автор')
    content = models.TextField(blank=True, verbose_name='контент')
    dt_created = models.DateTimeField(default=timezone.now, verbose_name='дата создания')
    dt_publish = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='статус')
    tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-dt_publish']
        indexes = [
            models.Index(fields=['-dt_publish'])
        ]

    def get_absolute_url(self):
        return reverse(viewname='blog:post_detail', args=[self.dt_publish.year,
                                                          self.dt_publish.month,
                                                          self.dt_publish.day,
                                                          self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    name = models.CharField(max_length=255, verbose_name='имя пользователя')
    email = models.EmailField(verbose_name='эл. почта')
    content = models.TextField(verbose_name='контент')
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    active = models.BooleanField(default=True, verbose_name='активен')

    objects = models.Manager()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['dt_created']
        indexes = [
            models.Index(fields=['dt_created'])
        ]

    def __str__(self):
        return f"Прокомментировал {self.name} пост \"{self.post}\""
