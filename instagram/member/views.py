from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username, password)
    return HttpResponse(username, password)


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('login')
    else:
        # Return an 'invalid login' error message.
        return print('invalid login')


def logout_view(request):
    logout(request)
