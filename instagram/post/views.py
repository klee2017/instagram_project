from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    photo = request.FILES.get('photo')
    if request.method == 'POST' and photo:
        photo = request.FILES['photo']
        post = Post.objects.create(photo=photo)
        return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        return render(request, 'post/post_create.html')

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
