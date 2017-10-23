from django.contrib.auth import (get_user_model, login as django_login, logout as django_logout)
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.decorators import login_required
from .forms import SignupForm, LoginForm

User = get_user_model()


# help 함수

def login(request):
    next_path = request.GET.get('next')

    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            if next_path:
                return redirect(next_path)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credential invalid')
    else:
        form = LoginForm()
    context = {
        'login_form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('post:post_list')
    else:
        form = SignupForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'member/signup.html', context)


@login_required
def profile(request):
    return HttpResponse()
