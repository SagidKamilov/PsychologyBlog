from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count

from psyhologyblog.settings import EMAIL_HOST_USER
from .models import Post, Tag
from .forms import EmailPostForm, CommentForm


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render(request=request, template_name='blog/post_comment.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} рекомендует " \
                      f"{post.title}"
            message = f"Прочти статью {post.title} по ссылке {post_url}\n\n" \
                      f"{cd['name']} комментирует: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER,
                      recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request=request, template_name='blog/post_share.html', context=context)


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, per_page=3)
    page_number = request.GET.get(key='page', default=1)
    page_obj = paginator.page(number=page_number)

    context = {
        'posts': page_obj,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, dt_publish__year=year, dt_publish__month=month, dt_publish__day=day)
    tags = post.tags.all()
    same_posts = same_posts_find(post)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'tags': tags,
        'same_posts': same_posts
    }

    return render(request, template_name='blog/post_detail.html', context=context)


def same_posts_find(post: Post):
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-dt_publish')[:4]
    return similar_posts
