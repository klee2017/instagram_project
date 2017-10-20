from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # POST 요청의 경우 PostForm 인스턴스 생성 과정에서 request.POST, request.FILES를 사용.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # photo = request.FILES['photo']
            # post = Post.objects.create(photo=photo)
            return redirect('post:post_list')
    else:
        # get 요청의 경우 빈 PostForm 인스턴스를 생성해서 템플릿에 전달
        form = PostForm()

    # get 요청에서 이 부분이 무조건 실행
    # POST 요청에서 is_valid를 통과하지 못하면 이 부분이 실행
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied


def comment_create(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            next = request.GET.get('next', '').strip()
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post_pk)
    else:
        form = CommentForm()
    context = {'form': form, }
    return render(request, 'post/post_create.html', context)


def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()

    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')