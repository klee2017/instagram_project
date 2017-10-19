from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form':comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        # POST 요청의 경우 PostForm 인스턴스 생성 과정에서 request.POST, request.FILES를 사용.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(
                photo=form.cleaned_data['photo']
            )
            # photo = request.FILES['photo']
            # post = Post.objects.create(photo=photo)
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        # get 요청의 경우 빈 PostForm 인스턴스를 생성해서 템플릿에 전달
        form = PostForm()

    # get 요청에서 이 부분이 무조건 실행
    # POST 요청에서 is_valid를 통과하지 못하면 이 부분이 실행
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = PostComment.objects.create(post=post, content=form.cleaned_data['content'])
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        form = CommentForm()
    context = {'form': form, }
    return render(request, 'post/post_create.html', context)

    # PostComment = Post.objects.get(pk=post_pk)

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
