from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from psyhologyblog.settings import EMAIL_HOST_USER
from .models import Post, Comment
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
    return render(request=request, template_name='blog/post_comment.html', context={'post': post, 'form': form,
                                                                                    'comment': comment})


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
    return render(request=request, template_name='blog/post_share.html', context={'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, dt_publish__year=year, dt_publish__month=month,
                             dt_publish__day=day)

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, template_name='blog/post_detail.html', context={'post': post, 'comments': comments, 'form': form})
