from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from registration.forms import RegisterForm


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="/blog/posts")
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request=request, template_name='registration/register_page.html', context=context)
