from django.contrib.auth import logout, authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

User = get_user_model()


# help 함수


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            if User.objects.filter(username=username).exists():
                return HttpResponse(f'Username {username} is already exist')
            user = User.objects.create_user(username=username, password=password)
            return HttpResponse(f'{user.username}, {user.password}')
    return render(request, 'member/signup.html')


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
